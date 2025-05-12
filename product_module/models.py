from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from account_module.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='Category Title')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='Title in Url')
    is_active = models.BooleanField(default=False, verbose_name='Active / Inactive')
    is_delete = models.BooleanField(verbose_name='Deleted / Not Deleted')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='Product Brand')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='Title in Url')
    image = models.ImageField(upload_to='images/brands',verbose_name='Image',null=True,blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Active / Inactive')
    is_delete = models.BooleanField(verbose_name='Deleted / Not Deleted')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.title


class ProductDiscountTimer(models.Model):
    title = models.CharField(max_length=100,verbose_name='Title')
    start_time = models.DateTimeField(null=True,blank=True,verbose_name='Discount Start Time')
    end_time = models.DateTimeField(null=True,blank=True,verbose_name='Discount End Time')
    is_main = models.BooleanField(default=False,verbose_name='Main Discount')
    is_delete = models.BooleanField(default=False,verbose_name= 'Deleted / Not deleted')

    class Meta:
        verbose_name = 'Product Discount Timer'
        verbose_name_plural = 'Product Discounts Timer'

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='Product Title')
    category = models.ManyToManyField('ProductCategory',
                                      verbose_name='Product Categories',related_name='product_categories')
    brand = models.ForeignKey('ProductBrand', on_delete=models.CASCADE, verbose_name='Product Brand', null=True,
                              blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='Product Image')
    short_description = models.CharField(max_length=300, null=True, blank=True, db_index=True,
                                         verbose_name='Product Short Description')
    description = models.TextField(db_index=True, verbose_name='Product Description')
    price = models.IntegerField(verbose_name='Product Price')
    discount_percentage = models.IntegerField(null=True, blank=True,
                                              verbose_name='Discount Percentage(If has discount)')
    discount_timer = models.ForeignKey(ProductDiscountTimer,on_delete=models.DO_NOTHING,verbose_name='Discount Timer',null=True,blank=True)
    slug = models.SlugField(default="", db_index=True, null=False, blank=True, max_length=200, unique=True)
    is_active = models.BooleanField(default=False, verbose_name='Active / Inactive')
    is_delete = models.BooleanField(verbose_name='Deleted / Not Deleted')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('products_detail',args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_price_after_discount(self):
        if self.discount_percentage:
            return self.price - (self.price * self.discount_percentage // 100)
        return self.price

    def __str__(self):
        return f"{self.title} / {self.price}"






class ProductGallery(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE,verbose_name='Product')
    image = models.ImageField(upload_to='images/product-gallery',verbose_name='Product Images')

    class Meta:
        verbose_name = 'Product Images'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return self.product.title

class ProductComments(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE,verbose_name='Product')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='User')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Create Date')
    text = models.TextField(verbose_name='Comment Text')

    class Meta:
        verbose_name = 'Product Comment'
        verbose_name_plural = 'Product Comments'

    def __str__(self):
        return f'{self.user} / {self.product}'


class ProductVisits(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='Product',related_name='productvisits')
    ip = models.CharField(max_length=50,verbose_name='Client IP')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,verbose_name='User')

    class Meta:
        verbose_name = 'Product Visit'
        verbose_name_plural = 'Product Visits'

    def __str__(self):
        return f'{self.product.title} / {self.ip}'