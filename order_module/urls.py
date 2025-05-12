from django.urls import path

from order_module import views

urlpatterns = [
    path('add-to-order/',views.add_product_to_order,name='add_to_order'),
    path('payment-request/',views.payment_request,name='payment_request'),
    path('verify-payment/',views.verify_payment,name='verify_payment'),
]