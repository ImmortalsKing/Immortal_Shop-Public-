from django.contrib import messages
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView


from account_module.models import User
from blog_module.forms import BlogCommentsForm
from blog_module.models import Blog, BlogCategory, BlogTags, BlogGallery, BlogComments, BlogVisits
from site_module.models import SocialLinks
from utils.http_service import get_client_ip


# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blog_module/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        blog_categories = BlogCategory.objects.annotate(blogs_count=Count('blog_category')).filter(is_active=True,is_delete=False).all()
        show_blog_categories = blog_categories[:3]
        blog_slug = self.kwargs.get('slug')
        context['blog_categories'] = blog_categories
        context['show_blog_categories'] = show_blog_categories
        context['blog_tags'] = BlogTags.objects.filter(blog__slug=blog_slug).all()
        return context

    def get_queryset(self):
        query = super().get_queryset().filter(is_active=True,is_delete=False).order_by('-create_time_date')
        category = self.kwargs.get('cat')
        print(category)
        if category is not None:
            query = query.filter(categories__url_title__iexact=category)
        return query


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_module/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        blog_slug = self.kwargs.get('slug')
        loaded_blog = self.object
        blog_galleries = BlogGallery.objects.filter(blog__slug=blog_slug)[:2]
        previous_blog = Blog.objects.order_by('-id').filter(id__lt=loaded_blog.id,is_active=True,is_delete=False).first()
        next_blog = Blog.objects.order_by('id').filter(id__gt=loaded_blog.id,is_active=True,is_delete=False).first()
        comments = BlogComments.objects.order_by('-create_date').filter(parent=None,blog__slug=blog_slug).prefetch_related('blogcomments_set')
        comments_count = BlogComments.objects.filter(blog__slug=blog_slug).count()
        context['selected_blog'] = Blog.objects.filter(slug=blog_slug,is_active=True,is_delete=False).first()
        context['comments'] = comments
        context['comments_count'] = comments_count
        context['blog_galleries'] = blog_galleries
        context['previous_blog'] = previous_blog
        context['next_blog'] = next_blog
        context['form'] = BlogCommentsForm()
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited:bool = BlogVisits.objects.filter(blog__id=loaded_blog.id, ip__iexact=user_ip).exists()
        if not has_been_visited:
            new_visit = BlogVisits(blog_id=loaded_blog.id, user_id=user_id, ip=user_ip)
            new_visit.save()
        return context

    def post(self,request:HttpRequest,*args,**kwargs):
        form = BlogCommentsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            blog_slug = kwargs.get('slug')
            blog = Blog.objects.filter(slug=blog_slug).first()
            parent_id = request.POST.get('parent_id')
            if parent_id is None or parent_id == "":
                new_comment = BlogComments(blog=blog, user=request.user, text=text)
                new_comment.save()
                messages.success(request, 'Your comment has been successfully added.')
                return redirect(reverse('blog_detail',kwargs={'slug': blog_slug}))
            else:
                parent = BlogComments.objects.filter(id=parent_id).first()
                new_comment = BlogComments(blog=blog,user=request.user, text=text, parent=parent)
                new_comment.save()
                messages.success(request, 'Your comment has been successfully added.')
                return redirect(reverse('blog_detail',kwargs={'slug': blog_slug}))

        context = {
            'form' : form
        }
        return render(request,'blog_module/blog_detail.html',context)


def blog_sidebar_component(request,*args,**kwargs):
    social_links = SocialLinks.objects.filter(is_main_urls=True).first()
    most_visited_blogs = Blog.objects.filter(is_active=True,is_delete=False).annotate(blog_count=Count('visits')).order_by('-blog_count')[:4]
    blog_slug = kwargs.get('slug')
    is_blog_exists = Blog.objects.exists()
    super_author = None
    super_author_exists = User.objects.filter(is_superauthor=True).exists()
    if super_author_exists:
        super_author = User.objects.filter(is_superauthor=True).first()
    context = {
        'is_blog_exists': is_blog_exists,
        'super_author': super_author,
        'blog_tags' : BlogTags.objects.filter(blog__slug=blog_slug).all(),
        'blog_categories' : BlogCategory.objects.annotate(blogs_count=Count('blog_category')).filter(is_active=True,is_delete=False).all(),
        'most_visited_blogs' : most_visited_blogs,
        'social_links': social_links,
    }
    return render(request,'blog_module/components/blogs_sidebar.html',context)


def blog_info(request,blog,slug):
    user_ip = get_client_ip(request)
    blog_visits_count = BlogVisits.objects.filter(blog__slug=slug,ip=user_ip).count()
    context = {
        'blog_categories' : BlogCategory.objects.filter(is_active=True,is_delete=False),
        'blog' : blog,
        'comments_count' : BlogComments.objects.filter(blog__slug=slug).count(),
        'blog_visits_count' : blog_visits_count,
    }
    return render(request,'blog_module/components/blog_info.html',context)