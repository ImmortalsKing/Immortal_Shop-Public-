from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='products_list_by_category'),
    path('brand/<brand>', views.ProductListView.as_view(), name='products_list_by_brand'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='products_detail'),
    # path('add-product-comment', views.AddProductComment.as_view(), name='add_product_comment'),
    path('cat/',lambda request:redirect('products_list',permanent=True)),
    path('brand/',lambda request:redirect('products_list',permanent=True)),
    path('add-to-favorites/<slug:slug>',views.add_to_favorites,name='add_to_favorites'),
    path('remove-from-favorites/<slug:slug>',views.remove_from_favorites,name='remove_from_favorites'),
]
