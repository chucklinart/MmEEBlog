from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Blog, Promo
from .submodels.media import Video, Pic, Podcast
from .submodels.taxonomy import Category
from .submodels.people import Blogger
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from rest_framework import viewsets
from django import template
from markdownx.utils import markdownify


register = template.Library()
@register.filter
def markdown(text):
    return markdownify(text)
register.filter('markdown', markdown)

# pop stuff up in modals or in other ajaxy ways

class AjaxTemplateMixin(object): 
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
            if request.is_ajax():
                self.template_name = self.ajax_template_name
                return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)

class BlogList(ListView):
    model = Blog
    ordering = ('-posted' )
    template_name='blog_list.html'
    paginate_by = 10
    queryset = Blog.objects.all()
    context_object_name = 'blog_list'

class BlogDetailView(DetailView):
    template_name='blog_single.html'
    model = Blog

    @register.filter
    def markdown(text):
        return markdownify(text)
    register.filter('markdown', markdown)

class BloggerDetailView(DetailView):
    template_name = 'author_single.html'
    model = Blogger

class BloggerList(ListView):
    template_name = 'all_authors.html'
    model = Blogger
    ordering = ('user.last_name' )
    queryset = Blogger.objects.all()
    context_object_name = 'profile_list'

class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    paginate_by = 20
    queryset = Category.objects.all()
    context_object_name = 'category_list'

class CategoryBlogView(ListView):
    template_name='category_blog.html'
    paginate_by = 10
    
    def get_queryset():
        self.blog_category = get_object_or_404(Category, name=self.kwargs['blog_categories'])
        return Blog.objects.filter(blog_category=self.blog_category)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the category
        context['blog_category'] = self.blog_category
        return context
    context_object_name = 'blogs_by_category'

class VideoList(ListView):
    model = Video
    template_name='video_list.html'
    queryset = Video.objects.all()
    context_object_name = 'video_list'

class VideoDetailView(DetailView):
    template_name='video_single.html'
    model = Video

class PodcastList(ListView):
    model = Podcast
    template_name='podcast_list.html'
    queryset = Podcast.objects.all()
    context_object_name = 'podcast_list'

class PodcastDetailView(DetailView):
    template_name='podcast_single.html'
    model = Podcast

# Ads
class PromoDetailView(DetailView):
    template_name='promo.html'
    model = Promo

# LNTip popup
class LNTipView(AjaxTemplateMixin, TemplateView):
    template_name = 'lntip.html'

def update_blogger(request, user_id):
    user = User.objects.get(pk=user_id)
    user.blogger.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

 # CHANGEME or remove me
def handle404(request, exception):
    message = ["<i>hERPidty derp</i> -- page not found.  If you were looking for something in the past (some content on the old site), perhaps it has been archived in the Wayback Machine.  Try <a href='https://web.archive.org/web/*/http://chucklinart.com/blog'>there</a>."
    ]
    context = {
        'message': message[randint(0,2)]
    }
    return render(request, "404.html", context, status=404)
