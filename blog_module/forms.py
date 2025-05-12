from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from blog_module.models import BlogComments


class BlogCommentsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = BlogComments
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'class': "form-control",
                'id': "text",
                'placeholder': "Enter Comment Text...",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter Comment Text...'",
            }),
        }
        error_messages = {
            'text': {
                'required': 'Enter your comment please'
            }
        }
