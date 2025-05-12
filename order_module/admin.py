from django.contrib import admin

from order_module.models import Order, OrderDetails, ShippingMethod


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','is_paid','payment_date']
    list_editable = ['is_paid']
    list_filter = ['is_paid','payment_date']

@admin.register(OrderDetails)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order' , 'product' , 'quantity' , 'final_price']


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_editable = ('price', 'is_active')