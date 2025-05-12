from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox,ReCaptchaV3


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id' : "email",
            'name' : "email",
            'placeholder': "Enter your email",
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': "username",
            'name': "username",
            'placeholder': "Enter your username",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label= 'Password',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'id' : "password",
            'name' : "password",
            'placeholder': "Enter your password",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password_confirm = forms.CharField(
        label= 'Password Confirm',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'id' : "password_confirm",
            'name' : "password_confirm",
            'placeholder': "Enter your password again",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            return password_confirm
        raise ValidationError('Password and Password confirm are different!')


class LoginForm(forms.Form):
    identification = forms.CharField(
        label= 'Email or Username',
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'id': "identification",
            'name': "identification",
            'placeholder': "Enter your email or username",
        }),
        validators= [
            validators.MaxLengthValidator(150),
        ]
    )
    password = forms.CharField(
        label= 'Password',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "password",
            'name': "password",
            'placeholder': "Enter your password",
        }),
        validators= [
            validators.MaxLengthValidator(100)
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': "email",
            'name': "email",
            'placeholder': "Enter your email",
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "password",
            'name': "password",
            'placeholder': "Enter your password",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password_confirm = forms.CharField(
        label='Password Confirm',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "password_confirm",
            'name': "password_confirm",
            'placeholder': "Enter your password again",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            return password_confirm
        raise ValidationError('Password and Password confirm are different!')