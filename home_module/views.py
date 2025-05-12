import json
from os.path import exists

from django.contrib import messages
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.utils import ErrorList
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from blog_module.models import Blog
from product_module.models import Product, ProductDiscountTimer, ProductBrand
from home_module.forms import NewsletterSubscriberForm
from site_module.models import Slider, SiteSettings, SiteBanner, FAQ, FooterLink, FooterLinkBox, NewsletterSubscriber, \
    SocialLinks, TermsAndConditions
from utils.convertors import group_list
from utils.email_service import send_email


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discount_timer_products = Product.objects.filter(is_active=True,is_delete=False,discount_percentage__isnull=False,discount_timer__isnull=False)[:3]
        discount_timer = ProductDiscountTimer.objects.filter(is_delete=False,is_main=True).first()
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:8]
        sliders = Slider.objects.filter(is_active=True).all()
        main_page_address = reverse('home_page')
        brands = ProductBrand.objects.filter(is_active=True,is_delete=False,image__isnull=False)[:5]
        popular_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            product_visits=Count('productvisits')).order_by('-product_visits')[:8]
        context['latest_products'] = group_list(latest_products, size=8)
        context['popular_products'] = group_list(popular_products, size=8)
        context['brands'] = brands
        context['main_page_address'] = main_page_address
        context['discount_timer_products'] = discount_timer_products
        context['discount_timer'] = discount_timer
        context['sliders'] = sliders
        context['home_banner'] = SiteBanner.objects.filter(is_active=True,
                                                      position__iexact=SiteBanner.SiteBannerPosition.HomePage).first()
        context['gif_banner'] = SiteBanner.objects.filter(is_active=True,
                                                           position__iexact=SiteBanner.SiteBannerPosition.HomeGif).first()
        context['discount_banner'] = SiteBanner.objects.filter(is_active=True,
                                                      position__iexact=SiteBanner.SiteBannerPosition.DiscountTimer).first()
        context['first_cat_banner'] = SiteBanner.objects.filter(is_active=True,
                                                                position__iexact=SiteBanner.SiteBannerPosition.FirstCatImg).first()
        context['second_cat_banner'] = SiteBanner.objects.filter(is_active=True,
                                                                 position__iexact=SiteBanner.SiteBannerPosition.SecondCatImg).first()
        context['third_cat_banner'] = SiteBanner.objects.filter(is_active=True,
                                                                position__iexact=SiteBanner.SiteBannerPosition.ThirdCatImg).first()
        context['forth_cat_banner'] = SiteBanner.objects.filter(is_active=True,
                                                                position__iexact=SiteBanner.SiteBannerPosition.ForthCatImg).first()
        return context


def site_header_component(request: HttpRequest):
    settings = SiteSettings.objects.filter(is_main_setting=True).first()
    context = {
        'settings': settings
    }
    return render(request, 'shared/site_header_component.html', context)


def site_banner_component(request: HttpRequest):
    path_parts = str(request.path).split('/')
    url = path_parts[1].replace("-", " ").upper()
    address = request.path.rsplit('/', 1)
    new_address_1 = address[0] + '/'
    new_address_2 = request.path
    if len(path_parts) > 2:
        url_in = path_parts[2]
        if len(url_in) < 50 and url_in != 'cat' and url_in != 'brand':
            new_url_in = url_in.replace("-", " ").upper()
        else:
            new_url_in = ''
    else:
        new_url_in = ''
    context = {
        'url': url,
        'url_in': new_url_in,
        'address_1': new_address_1,
        'address_2': new_address_2,
    }
    return render(request, 'shared/site_banner_component.html', context)


from django.forms.utils import ErrorList
import json

def site_footer_component(request: HttpRequest):
    settings = SiteSettings.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    social_links = SocialLinks.objects.filter(is_main_urls=True).first()

    form_data = request.session.pop('newsletter_form_data', None)
    form_errors = request.session.pop('newsletter_form_errors', None)

    if form_data:
        form = NewsletterSubscriberForm(form_data)
        if form_errors:
            form._errors = form.errors.copy()
            for field, errors in json.loads(form_errors).items():
                form._errors[field] = ErrorList([e['message'] for e in errors])
    else:
        form = NewsletterSubscriberForm()

    context = {
        'settings': settings,
        'footer_link_boxes': footer_link_boxes,
        'form': form,
        'social_links': social_links,
    }
    return render(request, 'shared/site_footer_component.html', context)



def site_related_products_component(request: HttpRequest):
    products = Product.objects.filter(is_active=True, is_delete=False, discount_percentage__isnull=False , discount_timer__isnull=True)[:6]
    related_banner = SiteBanner.objects.filter(is_active=True,
                              position__iexact=SiteBanner.SiteBannerPosition.ProductList).first()
    context = {
        'products': products,
        'related_banner': related_banner,
    }
    return render(request, 'shared/related_product_component.html', context)


class AboutUsView(TemplateView):
    template_name = 'home_module/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['site_settings'] = SiteSettings.objects.prefetch_related('team_members').filter(
            is_main_setting=True).first()
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.AboutUs)
        return context


class FAQView(TemplateView):
    template_name = 'home_module/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['banner'] = SiteBanner.objects.filter(is_active=True,position__iexact=SiteBanner.SiteBannerPosition.FAQ).first()
        context['faqs'] = FAQ.objects.filter(is_active=True).all()
        return context


class SubscribeToNewsletter(View):
    def get(self, request):
        form_data = request.session.pop('newsletter_form_data', None)
        form_errors = request.session.pop('newsletter_form_errors', None)

        if form_data:
            form = NewsletterSubscriberForm(form_data)
            if form_errors:
                form._errors = form.errors.copy()
                for field, errors in json.loads(form_errors).items():
                    form._errors[field] = ErrorList([e['message'] for e in errors])
        else:
            form = NewsletterSubscriberForm()

        context = {
            'form': form
        }
        return render(request, 'shared/includes/subscribe.html', context)

    def post(self, request):
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            is_email_exists = NewsletterSubscriber.objects.filter(email=email).exists()
            if not is_email_exists:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'You Subscribed to the newsletter successfully.')
            else:
                messages.info(request, 'You are already subscribed.')
            return redirect(reverse('home_page'))

        # فرم نامعتبره، خطاها و داده‌ها رو ذخیره کن توی session
        request.session['newsletter_form_data'] = request.POST
        request.session['newsletter_form_errors'] = form.errors.as_json()
        return redirect(reverse('home_page'))


class RemoveFromNewsletter(View):
    def get(self,request, email):
        is_email_exists = NewsletterSubscriber.objects.filter(email=email).exists()
        if is_email_exists:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            subscriber.delete()
            messages.success(request,'You removed from the newsletter service successfully.')
            return redirect(reverse('home_page'))
        else:
            return Http404

class TermsAndConditionsView(TemplateView):
    template_name = 'home_module/terms&conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['terms'] = TermsAndConditions.objects.first()
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.TermsAndConditions)
        return context