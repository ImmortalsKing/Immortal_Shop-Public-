from urllib.parse import urljoin

from celery import group
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog_module.models import Blog
from blog_module.tasks import send_newsletter_email
from site_module.models import NewsletterSubscriber, SiteSettings
from utils.email_service import send_email


@receiver(post_save,sender=Blog)
def send_blog_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        subscribers = NewsletterSubscriber.objects.all()
        site_setting = SiteSettings.objects.filter(is_main_setting=True).first()
        site_url = site_setting.site_url if site_setting else 'http://localhost:8000'
        recipient_emails = [subscriber.email for subscriber in subscribers]

        # for email in recipient_emails:
        #     context = {
        #         'title': instance.title,
        #         'short_description': instance.short_description,
        #         'url': f'http://localhost:80/blogs/{instance.slug}',
        #         'email': email,
        #     }
        tasks = [
            send_newsletter_email.s(instance.title, email, {
                'title': instance.title,
                'short_description': instance.short_description,
                'url': urljoin(site_url, f'blogs/{instance.slug}'),
                'email': email,
            }) for email in recipient_emails
        ]
        group(*tasks).apply_async()
            # send_email(f'New Blog({instance.title})',to=email,context=context,template_name='emails/newsletter.html')