from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import time

from order_module.models import Order, OrderDetails
from product_module.models import Product
from django.conf import settings
import requests
import json


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "Finalizing your purchase from our site"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_product_to_order(request):
    product_id = request.GET.get('product_id')
    count = request.GET.get('count')

    if count is None or not count.isdigit() or int(count) < 1:
        return JsonResponse({
            'status':'invalid_count',
            'text':'Entered count not found.',
            'icon':'error',
            'confirm_button_text':'Ok',
        })

    count = int(count)

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            current_order , created = Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
            current_order_detail = current_order.orderdetails_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.quantity += count
                current_order_detail.save()
            else:
                new_detail = OrderDetails(product_id=product_id,order_id=current_order.id,quantity=count)
                new_detail.save()
            return JsonResponse({
                'status': 'success',
                'text': 'The product has been successfully added to your shopping cart.',
                'icon': 'success',
                'confirm_button_text': 'Ok',
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'The product not found.',
                'icon': 'error',
                'confirm_button_text': 'Ok',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'To add this product to your cart, please log in first.',
            'icon': 'warning',
            'confirm_button_text': 'login',
            'redirect_url': reverse('login_page'),
        })


@login_required
def payment_request(request: HttpRequest):
    current_order , created = Order.objects.filter(user_id=request.user.id , is_paid=False)
    total_price = current_order.sub_total_amount()
    total = total_price + current_order.shipping_method.price
    if total == 0:
        return redirect(reverse('user_basket_page'))
    data = {
        "MerchantID": MERCHANT,
        "Amount": total * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}

@login_required
def verify_payment(request:HttpRequest,authority):
    current_order, created = Order.objects.filter(user_id=request.user.id, is_paid=False)
    total_price = current_order.sub_total_amount()
    total = total_price + current_order.shipping_method.price
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_paid = True
            current_order.payment_date = time.time()
            current_order.save()
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response