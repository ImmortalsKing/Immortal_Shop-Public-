from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View

from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from account_module.models import User
from account_module.tasks import send_activation_email, send_reset_password_email
from utils.email_service import send_email


# Create your views here.

class RegisterView(View):
    def get(self, request: HttpRequest):
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'account_module/register_page.html', context)

    def post(self, request: HttpRequest):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password')
            user_email_exists = User.objects.filter(email__iexact=user_email).exists()
            user_username_exists = User.objects.filter(username__iexact=user_username).exists()
            if user_email_exists:
                form.add_error('email', 'The entered email is duplicate.')
            elif user_username_exists:
                form.add_error('username', 'The entered username is duplicate.')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_username
                )
                new_user.set_password(user_password)
                new_user.save()

                send_activation_email.delay(new_user.id)
                messages.success(request, 'Account created successfully. Please check your email to activate your account.')
                # send_email('Account Activation', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))
        context = {
            'form': form
        }
        return render(request, 'account_module/register_page.html', context)


class ActivateAccountView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'Your account has been activated successfully!')
                return redirect(reverse('login_page'))
            else:
                messages.info(request, 'Your account has already been activated')
                return redirect(reverse('login_page'))
        return Http404


class LoginView(View):
    def get(self, request: HttpRequest):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request: HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            identification = form.cleaned_data.get('identification')
            user_password = form.cleaned_data.get('password')
            user: User = User.objects.filter(Q(email__iexact=identification) | Q(username__iexact=identification)).first()
            if user is not None:
                if not user.is_active:
                    form.add_error('identification', 'Your account has not been activated. Please activate account to Login')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        form.add_error('identification', 'The password or email/username is incorrect.')
            else:
                form.add_error('identification', 'The password or email/username is incorrect.')
        context = {
            'form': form
        }
        return render(request, 'account_module/login_page.html', context)


class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        form = ForgotPasswordForm
        context = {
            'form': form
        }
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_reset_password_email.delay(user.id)
                messages.success(request, 'Recovery code has been sent to your email successfully.')
                # send_email('Password Recovery', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('home_page'))
            else:
                form.add_error('email', 'The Email is incorrect.')
        context = {
            'form': form
        }
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        form = ResetPasswordForm()
        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_password = form.cleaned_data.get('password')
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))
        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'account_module/reset_password.html', context)

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login_page'))
