import secrets
from datetime import datetime, time
from idlelib.debugobj import dispatch

from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, DetailView, ListView

from account_module.models import User
from order_module.models import Order, OrderDetails, ShippingMethod
from product_module.models import Product
from user_panel_module.forms import EditProfileForm, ChangePasswordForm, BillingDetailsForm
from user_panel_module.tasks import update_email
from utils.email_service import send_email


# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/dashboard.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = EditProfileForm(instance=current_user)
        context = {
            'form': form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            new_email = form.cleaned_data.get('email')
            if new_email != request.user.email:
                if not User.objects.filter(email=new_email).exists():
                    current_user.temp_email = new_email
                    form.instance.email = request.user.email
                    form.save()
                    current_user.save(update_fields=['temp_email'])
                    update_email.apply_async(args=[current_user.id, new_email])
                    # send_email('Update Email', new_email, {'user': current_user}, 'emails/update_email.html')
                    messages.success(request,
                                     'Confirmation link has been send to your new email, your email will be change after your confirmation.')
                    return redirect(reverse('edit_profile_page'))
                else:
                    messages.error(request, 'Selected email is already in use.')
                    return redirect(reverse('edit_profile_page'))
            else:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect(reverse('edit_profile_page'))
        context = {
            'form': form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/edit_profile.html', context)


@method_decorator(login_required, name='dispatch')
class ChangeEmailView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is not None:
            user.email = user.temp_email
            user.email_active_code = get_random_string(72)
            user.save()
            if user.is_authenticated:
                messages.success(request, 'Your email has been changed successfully.')
                return redirect(reverse('edit_profile_page'))
            else:
                login(request, user)
                messages.success(request, 'Your email has been changed successfully.')
                return redirect(reverse('edit_profile_page'))
        else:
            return Http404


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        form = ChangePasswordForm()
        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            check_password = request.user.check_password(current_password)
            if check_password:
                new_password = form.cleaned_data.get('new_password')
                if not request.user.check_password(new_password):
                    user = request.user
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return redirect(reverse('login_page'))
                else:
                    form.add_error('new_password', 'New password must be different from current one!')
            else:
                form.add_error('current_password',
                               'Entered value as current password is wrong, please enter your current password correctly.')
        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@method_decorator(login_required, name='dispatch')
class FavoriteProductsView(ListView):
    model = Product
    template_name = 'user_panel_module/favorite_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.user.favorite_products.all()
        return query


@login_required
def user_panel_sidebar_component(request):
    current_user = User.objects.filter(id=request.user.id).first()
    context = {
        'user': current_user
    }
    return render(request, 'user_panel_module/components/user_panel_sidebar_component.html', context)


@method_decorator(login_required, name='dispatch')
class UserBasketView(TemplateView):
    template_name = 'user_panel_module/user_basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,
                                                                                                  user_id=self.request.user.id)
        subtotal_amount = current_order.sub_total_amount()
        shipping_method = ShippingMethod.objects.filter(is_active=True).all()

        context['shipping_methods'] = shipping_method
        context['order'] = current_order
        context['subtotal'] = subtotal_amount
        return context


@login_required
def user_basket_remove_detail(request):
    detail_id = request.GET.get('detail_id')

    if detail_id is None:
        return JsonResponse({
            'status': 'detail_id_not_found',
            'text': 'There is no product with these specifications.',
            'icon': 'error',
            'confirm_button_text': 'OK',
        })

    deleted_count, deleted_dict = OrderDetails.objects.filter(id=detail_id, order__is_paid=False,
                                                              order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found',
            'text': 'The desired product was not found.',
            'icon': 'error',
            'confirm_button_text': 'OK',
        })

    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    shipping_method = ShippingMethod.objects.filter(is_active=True).all()

    subtotal_amount = current_order.sub_total_amount()

    data = render_to_string('user_panel_module/user_basket_content.html', {
        'shipping_methods': shipping_method,
        'order': current_order,
        'subtotal': subtotal_amount,
    })
    return JsonResponse({
        'status': 'remove_success',
        'body': data,
        'text': 'The item was successfully removed from the shopping cart.',
        'icon': 'success',
        'confirm_button_text': 'OK',
    })


@login_required
def user_basket_change_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None and state is None:
        return JsonResponse({
            'status': 'detail_or_state_not_found',
            'text': 'The desired product or quantity was not found.',
            'icon': 'error',
            'confirm_button_text': 'OK',
        })

    order_detail = OrderDetails.objects.filter(id=detail_id, order__is_paid=False,
                                               order__user_id=request.user.id).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found',
            'text': 'The disired product was not found.',
            'icon': 'error',
            'confirm_button_text': 'OK',
        })

    if state == 'increase':
        order_detail.quantity += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.quantity == 1:
            order_detail.delete()
        else:
            order_detail.quantity -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid',
            'text': 'Entered quantity is invalid.',
            'icon': 'error',
            'confirm_button_text': 'OK',
        })

    current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    shipping_method = ShippingMethod.objects.filter(is_active=True).all()

    subtotal_amount = current_order.sub_total_amount()

    data = render_to_string('user_panel_module/user_basket_content.html', {
        'shipping_methods': shipping_method,
        'order': current_order,
        'subtotal': subtotal_amount,
    })
    return JsonResponse({
        'status': 'success',
        'body': data,
    })


# region def shipping

# def set_shipping_method(request):
#     if request.method == 'POST':
#         shipping_id = request.POST.get('shipping_method')
#
#         if shipping_id is None:
#             return JsonResponse({
#                 'status': 'shipping_method_not_found',
#                 'text': 'The desired shipping method was not found.',
#                 'icon': 'error',
#                 'confirm_button_text': 'OK',
#             })
#
#         shipping = ShippingMethod.objects.filter(id=shipping_id, is_active=True).first()
#
#         if shipping is None:
#             return JsonResponse({
#                 'status': 'shipping_method_not_found',
#                 'text': 'The desired shipping method was not found.',
#                 'icon': 'error',
#                 'confirm_button_text': 'OK',
#             })
#
#         current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(is_paid=False,
#                                                                                                   user_id=request.user.id)
#
#         current_order.shipping_method = shipping
#         current_order.save()
#
#         shipping_method = ShippingMethod.objects.filter(is_active=True).all()
#
#         subtotal_amount = current_order.sub_total_amount()
#
#         data = render_to_string('user_panel_module/user_basket_content.html', {
#             'shipping_methods': shipping_method,
#             'order': current_order,
#             'subtotal': subtotal_amount,
#         })
#         return JsonResponse({
#             'status': 'success',
#             'body': data,
#             'text': 'The Shipping Method has been setted successfully.',
#             'icon': 'success',
#             'confirm_button_text': 'OK',
#         })

# endregion

@method_decorator(login_required, name='dispatch')
class OrderCheckoutView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = BillingDetailsForm(instance=current_user)

        current_order, created = Order.objects.prefetch_related('orderdetails_set').get_or_create(
            is_paid=False,
            user_id=request.user.id
        )

        subtotal_amount = current_order.sub_total_amount()
        shipping_method = ShippingMethod.objects.filter(is_active=True).all()
        total = subtotal_amount + current_order.shipping_method.price if current_order.shipping_method else subtotal_amount

        context = {
            'form': form,
            'order': current_order,
            'subtotal': subtotal_amount,
            'total': total,
            'shipping_methods': shipping_method,
        }
        return render(request, 'user_panel_module/order_checkout.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        form = BillingDetailsForm(instance=current_user)
        current_order = Order.objects.filter(is_paid=False, user=request.user.id).first()

        if not current_order:
            messages.error(request, 'No active order found.')
            return redirect(reverse('order_checkout'))

        if 'submit_1' in request.POST:
            print('dool')
            shipping_id = request.POST.get('shipping_method')
            form = BillingDetailsForm(request.POST, instance=current_user)
            if form.is_valid():
                if shipping_id:
                    shipping = ShippingMethod.objects.filter(id=shipping_id, is_active=True).first()
                    if shipping:
                        current_order.shipping_method = shipping
                        current_order.save()
                        form.save(commit=True)
                        messages.success(request, 'Billing details saved successfully.')
                        return redirect(reverse('order_checkout'))
                    else:
                        messages.error(request, 'Selected shipping method is invalid.')
                else:
                    messages.error(request, 'You should select one shipping method first.')

        elif 'submit_2' in request.POST:
            payment_method = request.POST.get('selector')
            order_id = request.POST.get('order_id')

            if not payment_method:
                messages.error(request, 'You should select one payment method.')
                return redirect(reverse('order_checkout'))

            elif payment_method == 'door_to_door':
                return redirect(reverse('successful_purchase', args=[order_id]))

            elif payment_method == 'paypal':
                return redirect(reverse('fail_purchase'))

        subtotal_amount = current_order.sub_total_amount()
        shipping_method = ShippingMethod.objects.filter(is_active=True).all()
        total = subtotal_amount + current_order.shipping_method.price if current_order.shipping_method else subtotal_amount

        context = {
            'form': form,
            'order': current_order,
            'subtotal': subtotal_amount,
            'total': total,
            'shipping_methods': shipping_method,
        }
        return render(request, 'user_panel_module/order_checkout.html', context)


@method_decorator(login_required, name='dispatch')
class SuccessfulPurchaseView(View):
    def process_payment(self, request, order_id):
        order: Order = Order.objects.filter(id=order_id, is_paid=False, user_id=request.user.id).first()

        if order is not None:
            all_details = OrderDetails.objects.filter(order_id=order_id).all()
            for detail in all_details:
                price = detail.get_total_price()
                detail.final_price = price
                detail.save()
            order.is_paid = True
            order.payment_date = datetime.now()
            order.tracking_code = ''.join(str(secrets.randbelow(10)) for _ in range(18))
            order.save()
        else:
            raise ValidationError('The desired order is invalid.')

        tracking_code = order.tracking_code
        context = {
            'tracking_code': tracking_code
        }
        return render(request, 'user_panel_module/successful_purchase.html', context)

    def post(self, request, order_id):
        return self.process_payment(request, order_id)

    def get(self, request, order_id):
        return self.process_payment(request, order_id)

@method_decorator(login_required, name='dispatch')
class FailedPurchaseView(View):
    def get(self, request):
        return render(request, 'user_panel_module/fail_purchase.html')


@method_decorator(login_required, name='dispatch')
class MyShoppingPageView(ListView):
    model = Order
    template_name = 'user_panel_module/my_shopping_page.html'
    context_object_name = 'my_shopping'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.prefetch_related('orderdetails_set').filter(user_id=self.request.user.id, is_paid=True)
        return query


@login_required
def my_shopping_detail(request: HttpRequest, order_id):
    order = Order.objects.prefetch_related('orderdetails_set').filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('The desired user basket was not found.')
    context = {
        'order': order
    }
    return render(request, 'user_panel_module/my_shopping_details_page.html', context)
