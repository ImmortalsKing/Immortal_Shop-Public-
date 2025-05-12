from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox

from product_module.models import ProductComments


class ProductCommentsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = ProductComments
        fields = ['text']
        widgets = {
            'text' : forms.Textarea(attrs={
                'class': 'form-control',
                'id': "comment",
                'name': "comment",
                'placeholder': "Enter your Comment ...",
            })
        }
        error_messages = {
            'text' : {
                'required' : 'Enter your comment please'
            }
        }