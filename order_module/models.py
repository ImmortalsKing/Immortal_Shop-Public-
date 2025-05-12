from django.db import models

from account_module.models import User
from product_module.models import Product


class ShippingMethod(models.Model):
    name = models.CharField(max_length=200, verbose_name='Shipping Name')
    price = models.IntegerField(verbose_name='Shipping Price')
    is_active = models.BooleanField(verbose_name='Active / Inactive')

    class Meta:
        verbose_name = 'Shipping Method'
        verbose_name_plural = 'Shipping Methods'

    def __str__(self):
        return f'{self.name} : ${self.price}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    is_paid = models.BooleanField(verbose_name='Is paid / Is not paid')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='Payment Date')
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, verbose_name='Shipping Method',
                                        null=True, blank=True)
    tracking_code = models.CharField(max_length=20, verbose_name='Tracking Code', null=True, blank=True)

    class Meta:
        verbose_name = 'User Order'
        verbose_name_plural = 'User Orders'

    def sub_total_amount(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetails_set.all():
                total_amount += order_detail.final_price * order_detail.quantity
        else:
            for order_detail in self.orderdetails_set.all():
                if order_detail.product.discount_percentage:
                    total_amount += order_detail.product.get_price_after_discount() * order_detail.quantity
                else:
                    total_amount += order_detail.product.price * order_detail.quantity
        return total_amount

    def __str__(self):
        return str(self.user)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    final_price = models.IntegerField(verbose_name='Final Price', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Quantity',default=1)

    def get_total_price(self):
        if self.product.discount_percentage:
            return self.product.get_price_after_discount() * self.quantity
        else:
            return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return str(self.order)
