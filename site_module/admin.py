from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

from account_module.models import User
from site_module import models
from site_module.models import SiteSettings, SiteBanner, TermsAndConditions
from django import forms

# Register your models here.

admin.site.register(models.Slider)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name','site_url','is_main_setting']
    filter_horizontal = ['team_members']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'team_members':
            kwargs['queryset'] = User.objects.filter(is_superuser=True)
        return super().formfield_for_manytomany(db_field, request,**kwargs)


@admin.register(SiteBanner)
class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title','url','position','is_active']
    list_editable = ['is_active']


class TACAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = TermsAndConditions
        fields = '__all__'

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    form = TACAdminForm
    list_display = ['title']

admin.site.register(models.FAQ)
admin.site.register(models.FooterLinkBox)
admin.site.register(models.FooterLink)
admin.site.register(models.SocialLinks)
admin.site.register(models.NewsletterSubscriber)

