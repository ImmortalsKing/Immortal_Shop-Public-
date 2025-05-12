from django.contrib import admin
from django.utils.safestring import mark_safe

from contact_module.models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['subject','full_name','email','is_read_by_admin','image_preview']
    list_editable = ['is_read_by_admin']
    readonly_fields = ['image_preview']


    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<a href="{obj.image.url}" target="_blank">'
                f'<img src="{obj.image.url}" style="max-width: 100px; max-height: 100px;" />'
                f'</a>'
            )
        return 'No Image'
    image_preview.short_description = "Image Preview"