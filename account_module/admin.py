from django.contrib import admin

from account_module.models import User
from product_module.models import Product


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','is_active']
    filter_horizontal = ['favorite_products']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'favorite_products':
            kwargs['queryset'] = Product.objects.filter(is_active=True,is_delete=False)
        return super().formfield_for_manytomany(db_field, request)
