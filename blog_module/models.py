from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from account_module.models import User


class BlogCategory(models.Model):
    title = models.CharField(max_length=200,db_index=True,verbose_name='Title')
    url_title = models.CharField(max_length=200,db_index=True,verbose_name='Url Title')
    image = models.ImageField(upload_to='images/blogs',verbose_name='Image')
    short_description = models.CharField(max_length=45 , verbose_name='Short Description')
    is_active = models.BooleanField(verbose_name='Active / Inactive')
    is_delete = models.BooleanField(verbose_name='Deleted / Not Deleted',default=False)

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blogs Categories'

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200,db_index=True,verbose_name='Title')
    image = models.ImageField(upload_to='images/blogs',verbose_name='Image')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author',verbose_name='Author')
    short_description = models.TextField(verbose_name='Short Description')
    text = RichTextUploadingField(verbose_name='Text')
    quotes = models.TextField(verbose_name='Quotes',null=True,blank=True)
    categories = models.ManyToManyField(BlogCategory,related_name='blog_category',verbose_name='Blog Categories')
    create_date = models.DateField(auto_now_add=True, verbose_name='Create Date')
    create_time_date = models.DateTimeField(auto_now_add=True,verbose_name='Create Time Date')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='Slug')
    is_active = models.BooleanField(verbose_name='Active / Inactive')
    is_delete = models.BooleanField(verbose_name='Deleted / Not Deleted',default=False)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return f'{self.title} / {self.author}'

    def get_absolute_url(self):
        return reverse('blog_detail',args=[self.slug])


class BlogTags(models.Model):
    caption = models.CharField(max_length=200,db_index=True,verbose_name='Caption')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_tags',verbose_name='Related Blog')

    class Meta:
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blogs Tags'

    def __str__(self):
        return self.caption


class BlogGallery(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='Blog')
    image = models.ImageField(upload_to='images/blog_gallery')

    class Meta:
        verbose_name = 'Blog Gallery'
        verbose_name_plural = 'Blog Galleries'

    def __str__(self):
        return str(self.blog)


class BlogComments(models.Model):
    parent = models.ForeignKey('BlogComments',null=True,blank=True,on_delete=models.CASCADE,verbose_name='Comments parent')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='Blog')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='User')
    text = models.TextField(db_index=True,verbose_name='Comment Text')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='Create Date')

    class Meta:
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blogs Comments'

    def __str__(self):
        return f'{self.user} / {self.blog}'


class BlogVisits(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='Blog',related_name='visits')
    ip = models.CharField(max_length=50,verbose_name='Client IP')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,verbose_name='User')

    class Meta:
        verbose_name = 'Blog Visit'
        verbose_name_plural = 'Blog Visits'

    def __str__(self):
        return f'{self.blog.title} / {self.ip}'