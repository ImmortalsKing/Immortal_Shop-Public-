from django.shortcuts import redirect
from django.urls import path

from user_panel_module import views

urlpatterns = [
    path('dashboard/', views.UserPanelDashboardPage.as_view(), name='user_dashboard'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile_page'),
    path('change-email/<active_code>', views.ChangeEmailView.as_view(), name='change_email_confirmation'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('favorite-products/', views.FavoriteProductsView.as_view(), name='favorite_products'),
    path('user-basket/', views.UserBasketView.as_view(), name='user_basket_page'),
    path('remove-order-detail/', views.user_basket_remove_detail, name='remove_order_detail'),
    path('change-order-count/', views.user_basket_change_count, name='change_order_count'),
    path('order-checkout/', views.OrderCheckoutView.as_view(), name='order_checkout'),
    path('successful-purchase/<int:order_id>' , views.SuccessfulPurchaseView.as_view(), name='successful_purchase'),
    path('fail-purchase/' , views.FailedPurchaseView.as_view(), name='fail_purchase'),
    path('my-shopping/' , views.MyShoppingPageView.as_view(), name='my_shopping_page'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='user_shopping_detail_page'),
    # path('set-shipping-method', views.set_shipping_method, name='set_shipping_method'),
]
