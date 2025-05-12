from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox

from account_module.models import User


class EditProfileForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'about_user', 'address', 'phone', 'fax', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your first name",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your first name'"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your last name",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your last name'"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your email",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your email'"
            }),

            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Tell about yourself",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Tell about yourself'",
                'rows': 3
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Enter your address",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your address'"
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your phone",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your phone'"
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your fax",
                'onfocus': "this.placeholder = ''",
                'onblur': "this.placeholder = 'Enter your fax'"
            }),
            'avatar': forms.FileInput(),
        }
        error_messages = {
            'email': {
                'required': 'Please enter your email'
            }
        }
        labels = {
            'username': 'User name(Cannot be changed)'
        }


class ChangePasswordForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    current_password = forms.CharField(
        label='Current Password: ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "current-password",
            'name': "current-password",
            'placeholder': "Enter your current password",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "new-password",
            'name': "new-password",
            'placeholder': "Enter your new password",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    new_password_confirm = forms.CharField(
        label='New Password Confirm',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "new-password-confirm",
            'name': "new-password-confirm",
            'placeholder': "Enter your new password again",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password == new_password_confirm:
            return new_password_confirm
        raise ValidationError('Password and Password confirm are different!')


class BillingDetailsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'phone', 'email', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your first name",
                'required':'True'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your last name",
                'required': 'True'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter your phone",
                'required': 'True'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'required': 'True'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Enter your address",
                'required': 'True'
            }),
        }