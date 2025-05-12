from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from account_module.models import User


# Create your models here.


class TermsAndConditions(models.Model):
    title = models.CharField(max_length=200,verbose_name='Title')
    text = RichTextUploadingField(verbose_name='Text')

    def __str__(self):
        return self.title

class SocialLinks(models.Model):
    title = models.CharField(max_length=200,verbose_name='Title')
    instagram_url = models.URLField(max_length=300,verbose_name='Instagram Url')
    github_url = models.URLField(max_length=300,verbose_name='GitHub Url')
    is_main_urls = models.BooleanField(verbose_name='Is Main Urls / Is not Main Urls')

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100,db_index=True,verbose_name='Site Name')
    site_url = models.URLField(max_length=200,db_index=True,verbose_name='Site URL')
    country_and_city = models.CharField(max_length=200,verbose_name='Country/City')
    address = models.CharField(max_length=200,verbose_name='Address')
    phone = models.CharField(max_length=100,verbose_name='Phone')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='Fax')
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name='Email')
    copy_right = models.TextField(verbose_name='Site CopyRight text')
    about_our_team = models.TextField(verbose_name='About Our Team',null=True,blank=True)
    about_us_text = models.TextField(verbose_name='About Us text')
    team_members = models.ManyToManyField(User,related_name='members',verbose_name='Team Members')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='Site Logo')
    social_urls = models.OneToOneField(SocialLinks,on_delete=models.CASCADE,verbose_name='Social Urls',null=True,blank=True)
    terms_and_conditions = models.ForeignKey(TermsAndConditions,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Terms & Conditions')
    is_main_setting = models.BooleanField(verbose_name='Main Settings')

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name


class Slider(models.Model):
    title = models.CharField(max_length=30,verbose_name='Title')
    image = models.ImageField(upload_to='images/sliders',verbose_name='Image')
    description = models.TextField(verbose_name='Description')
    url = models.URLField(max_length=300,verbose_name='URL')
    is_active = models.BooleanField(verbose_name='Active / Inactive')

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        HomePage = 'home_page' , 'Home Page'
        HomeGif = 'home_gif' , 'Home Gif'
        DiscountTimer = 'discount_timer' , 'Discount Timer'
        FAQ = 'faq' , 'FAQ'
        TermsAndConditions = 'terms_and_conditions' , 'TermsAndConditions'
        ProductList = 'products_list' , 'Products List Page'
        AboutUs = 'about_us' , 'About Us Page'
        FirstCatImg = 'home_page_first' , 'Home Page First Cat Image'
        SecondCatImg = 'home_page_second' , 'Home Page Second Cat Image'
        ThirdCatImg = 'home_page_third' , 'Home Page Third Cat Image'
        ForthCatImg = 'home_page_forth' , 'Home Page Forth Cat Image'

    title = models.CharField(max_length=200, verbose_name='Title')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='Url')
    image = models.ImageField(verbose_name='Image', upload_to='images/banners')
    is_active = models.BooleanField(verbose_name='Active / Inactive', default=False)
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='Position')

    class Meta:
        verbose_name = 'Site Banner'
        verbose_name_plural = 'Site Banners'

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=200,db_index=True,verbose_name='Question')
    answer = models.TextField(verbose_name='Answer',db_index=True)
    is_active = models.BooleanField(verbose_name='Active / Inactive')

    class Meta:
        verbose_name = 'Frequently Answer Question'
        verbose_name_plural = 'Frequently Answers Questions'

    def __str__(self):
        return self.question


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')

    class Meta:
        verbose_name = 'Footer Link Box'
        verbose_name_plural = 'Footer Link Boxes'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    url = models.URLField(max_length=500, verbose_name='Url')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='Footer Link Box')

    class Meta:
        verbose_name = 'Footer Link'
        verbose_name_plural = 'Footer Links'

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True,verbose_name='Email')
    date_subscribed = models.DateTimeField(auto_now_add=True,verbose_name='Date Subscribed')

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return self.email