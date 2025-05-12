from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms

from blog_module.models import Blog, BlogCategory, BlogTags, BlogGallery, BlogComments


class BlogAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ['title','author','create_date','is_active','is_delete']
    list_editable = ['is_active','is_delete']
    list_filter = ['categories','is_active']

    prepopulated_fields = {
        'slug' : ['title']
    }

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['title','is_active']
    list_editable = ['is_active']


@admin.register(BlogTags)
class BlogTagsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'blog']
    list_filter = ['blog']


admin.site.register(BlogGallery)
admin.site.register(BlogComments)