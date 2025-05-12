from django.contrib import admin

from product_module import models
from product_module.models import Product, ProductCategory, ProductBrand


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','is_active','is_delete']
    list_editable = ['price','is_active','is_delete']
    list_filter = ['category','is_active']
    prepopulated_fields = {
        'slug': ['title']
    }

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_delete']
    list_editable = ['url_title', 'is_active', 'is_delete']
    list_filter = ['is_active']

@admin.register(ProductBrand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active', 'is_delete']
    list_editable = ['url_title', 'is_active', 'is_delete']
    list_filter = ['is_active']

admin.site.register(models.ProductGallery)
admin.site.register(models.ProductComments)
admin.site.register(models.ProductDiscountTimer)