from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars', verbose_name='User Avatar', null=True, blank=True)
    about_user = models.TextField(null=True, blank=True, verbose_name='About User')
    email_active_code = models.CharField(max_length=300, verbose_name='User Email Active Code')
    address = models.TextField(null=True, blank=True, verbose_name='User Address')
    phone = models.CharField(max_length=50,null=True,blank=True,verbose_name='Phone Number')
    fax = models.CharField(max_length=50,null=True,blank=True,verbose_name='Fax')
    position = models.CharField(max_length=200,verbose_name='Position',null=True,blank=True)
    is_superauthor = models.BooleanField(verbose_name='Is Super Author',default=False)
    temp_email = models.EmailField(verbose_name='Temporary Email',null=True,blank=True)
    favorite_products = models.ManyToManyField('product_module.Product', related_name='favorited_by', blank=True,
                                               verbose_name='Favorite Products')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        # if self.first_name is not "" and self.last_name is not "":
        #     return self.get_full_name()
        return self.username