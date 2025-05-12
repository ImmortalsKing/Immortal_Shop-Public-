from django.db import models

# Create your models here.

class ContactUs(models.Model):
    subject = models.CharField(max_length=200,db_index=True,verbose_name='Subject')
    email = models.EmailField(max_length=200,verbose_name='Email')
    full_name = models.CharField(max_length=200,verbose_name='Full Name')
    message = models.TextField(verbose_name='Text')
    image = models.ImageField(upload_to='images/contact_us',verbose_name='Images',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Create Date')
    response = models.TextField(verbose_name='Response')
    is_read_by_admin = models.BooleanField(default=False,verbose_name='Read / Unread')

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us List'

    def __str__(self):
        return f'{self.subject} / {self.full_name}'