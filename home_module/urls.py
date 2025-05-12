from django.urls import path

from home_module import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home_page'),
    path('about-us/',views.AboutUsView.as_view(),name='about_us_page'),
    path('faq/',views.FAQView.as_view(),name='faq_page'),
    path('terms-and-conditions/',views.TermsAndConditionsView.as_view(),name='terms_and_conditions_page'),
    path('subscribe/',views.SubscribeToNewsletter.as_view(),name='subscribe_to_newsletter'),
    path('remove-subscription/<str:email>',views.RemoveFromNewsletter.as_view(),name='remove_subscription'),
]