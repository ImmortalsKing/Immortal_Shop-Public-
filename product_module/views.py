from django.contrib import messages
from django.core.paginator import InvalidPage, EmptyPage
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, View

from product_module.forms import ProductCommentsForm
from product_module.models import Product, ProductCategory, ProductBrand, ProductGallery, ProductComments, ProductVisits
from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip


class ProductListView(ListView):
    template_name = 'product_module/products_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']

    def get_paginate_by(self, queryset):
        allowed_values = [1, 3, 6]
        paginate_by = self.request.GET.get('paginate_by', 1)
        try:
            paginate_by = int(paginate_by)
        except ValueError:
            paginate_by = 1
        if paginate_by in allowed_values:
            return paginate_by
        return 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['paginate_by'] = self.get_paginate_by(self.get_queryset())
        context['banner'] = SiteBanner.objects.filter(is_active=True,position__iexact=SiteBanner.SiteBannerPosition.ProductList).first()
        return context

    def get_queryset(self):
        query = super().get_queryset()
        category = self.kwargs.get('cat')
        brand = self.kwargs.get('brand')
        start_price = self.request.GET.get('start_price')
        end_price = self.request.GET.get('end_price')

        if start_price is not None:
            query = query.filter(price__gte=float(start_price))
        if end_price is not None:
            query = query.filter(price__lte=float(end_price))
        if category is not None:
            query = query.filter(category__url_title__iexact=category)
        if brand is not None:
            query = query.filter(brand__url_title__iexact=brand)

        return query

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        paginate_by = self.get_paginate_by(self.object_list)

        paginator = self.get_paginator(self.object_list, paginate_by)
        page_number = self.request.GET.get(self.page_kwarg, 1)

        try:
            # Check if the requested page exists
            paginator.page(page_number)
        except (EmptyPage, ValueError):
            # If the page does not exist, redirect to the first page
            query_params = self.request.GET.copy()
            query_params[self.page_kwarg] = 1
            return HttpResponseRedirect(f"{reverse('products_list')}?{query_params.urlencode()}")

        return super().get(request, *args, **kwargs)
        # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        #     products = self.get_queryset()
        #     return render(request, 'product_module/products_list.html', {'products': products})
        # return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    template_name = 'product_module/products_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries'] = group_list(galleries)
        context['comments'] = ProductComments.objects.order_by('-create_date').filter(product_id=loaded_product.id)
        context['comments_count'] = ProductComments.objects.filter(product_id=loaded_product.id).count()
        context['form'] = ProductCommentsForm()
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisits.objects.filter(product_id=loaded_product.id,ip__iexact=user_ip).exists()
        if not has_been_visited:
            new_visit = ProductVisits(product_id=loaded_product.id,user_id=user_id,ip=user_ip)
            new_visit.save()
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()
        form = ProductCommentsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            product_slug = self.kwargs.get('slug')
            product = Product.objects.filter(slug=product_slug).first()
            new_comment = ProductComments(product=product, user=request.user, text=text)
            new_comment.save()
            messages.success(request, 'Your comment has been successfully added.')
            return redirect(reverse('products_detail', args=[product_slug]))

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

def product_category_component(request: HttpRequest):
    main_categories = ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(
        is_active=True, is_delete=False)
    context = {
        'main_categories': main_categories
    }
    return render(request, 'product_module/components/product_category_component.html', context)


def product_brand_component(request: HttpRequest):
    main_brands = ProductBrand.objects.annotate(brands_count=Count('product')).filter(is_active=True, is_delete=False)
    context = {
        'main_brands': main_brands
    }
    return render(request, 'product_module/components/product_brand_component.html', context)


# def add_product_comment(request: HttpRequest):
#     if request.user.is_authenticated:
#         product_comment = request.GET.get('product_comment')
#         product_id = request.GET.get('product_id')
#         print(product_id, product_comment)
#         new_comment = ProductComments(product_id=product_id, text=product_comment, user_id=request.user.id)
#         new_comment.save()
#         context = {
#             'comments': ProductComments.objects.order_by('-create_date').filter(product_id=product_id),
#             'comments_count': ProductComments.objects.filter(product_id=product_id).count()
#         }
#         return render(request,'includes/product_comments_partial.html',context)
#     return HttpResponse('response')


def add_to_favorites(request: HttpRequest, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    if product in user.favorite_products.all():
        messages.info(request, f'{product.title} is already in your favorites.')
    else:
        user.favorite_products.add(product)
        messages.success(request, f'{product.title} added to your favorites.')

    referer_url = request.META.get('HTTP_REFERER')
    if referer_url and f'/products/{product.slug}' in referer_url:
        return redirect(reverse('products_detail', kwargs={'slug': product.slug}))
    elif referer_url and '/account/favorite-products' in referer_url:
        return redirect(reverse('favorite_products'))
    elif referer_url and '/products/' in referer_url:
        return redirect(reverse('products_list'))
    elif referer_url and '' in referer_url:
        return redirect(reverse('home_page'))


def remove_from_favorites(request: HttpRequest , slug):
    user = request.user
    product = get_object_or_404(Product , slug=slug)
    if product in user.favorite_products.all():
        user.favorite_products.remove(product)
        messages.success(request, f'{product.title} removed from your favorites.')
    else:
        messages.info(request, f'{product.title} is not in your favorites.')

    referer_url = request.META.get('HTTP_REFERER')
    if referer_url and f'/products/{product.slug}' in referer_url:
        return redirect(reverse('products_detail', kwargs={'slug': product.slug}))
    elif referer_url and '/account/favorite-products' in referer_url:
        return redirect(reverse('favorite_products'))
    elif referer_url and '/products/' in referer_url:
        return redirect(reverse('products_list'))
    elif referer_url and '' in referer_url:
        return redirect(reverse('home_page'))

