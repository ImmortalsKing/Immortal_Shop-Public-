from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from contact_module.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = ContactUs
        fields = ['full_name','email','subject','message','image']
        widgets = {
            'full_name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter your name",
                'onfocus' : "this.placeholder = ''",
                'onblur' : "this.placeholder = 'Enter your name'"
            }),
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter your email",
                'onfocus' : "this.placeholder = ''",
                'onblur' : "this.placeholder = 'Enter your email'"
            }),
            'subject' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : "Enter your subject",
                'onfocus' : "this.placeholder = ''",
                'onblur' : "this.placeholder = 'Enter your subject'"
            }),
            'message' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : 2,
                'placeholder' : "Enter your message",
                'onfocus' : "this.placeholder = ''",
                'onblur' : "this.placeholder = 'Enter your name'"
            }),
            'image' : forms.FileInput()
        }
        error_messages = {
            'full_name' : {
                'required': 'Enter your full name please',
            },
            'email': {
                'required': 'Enter your email please'
            },
            'subject': {
                'required': 'Enter your subject please'
            },
            'message': {
                'required': 'Enter your message please'
            },
        }