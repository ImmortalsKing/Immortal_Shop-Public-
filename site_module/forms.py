# from django import forms
# from django.core import validators
#
#
# class NewsletterSubscriberForm(forms.Form):
#     email = forms.EmailField(
#         label='Your Email',
#         widget=forms.EmailInput(attrs={
#             'class': "form-control",
#             'name': "EMAIL",
#             'placeholder': "Enter Email",
#             'onfocus': "this.placeholder = ''",
#             'onblur': "this.placeholder = 'Enter Email '",
#             'required': "",
#             'type': "email",
#         }),
#         validators=[
#             validators.MaxLengthValidator(100),
#             validators.EmailValidator
#         ]
#     )
