from django.shortcuts import redirect
from django.urls import path

from blog_module import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blogs_list'),
    path('<slug:slug>', views.BlogDetailView.as_view(), name='blog_detail'),
    path('cat/<cat>', views.BlogListView.as_view(), name='blogs_list_by_category'),
    path('cat/', lambda request: redirect('blogs_list', permanent=True)),
]
