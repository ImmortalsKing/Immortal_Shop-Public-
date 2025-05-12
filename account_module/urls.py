from django.urls import path

from account_module import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register_page'),
    path('login/',views.LoginView.as_view(),name='login_page'),
    path('logout/',views.LogoutView.as_view(),name='logout_page'),
    path('forgot-password/',views.ForgotPasswordView.as_view(),name='forgot_pass_page'),
    path('reset-password/<active_code>',views.ResetPasswordView.as_view(),name='reset_password_page'),
    path('activate-account/<email_active_code>',views.ActivateAccountView.as_view(),name='activate_account')
]