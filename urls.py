from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from markdownx import urls as markdownx
from . import views
from . import feeds

app_name = 'mmeeblog'

urlpatterns = [
    path('videos/', views.VideoList.as_view(), name='videos'),
    path('videos/<slug:slug>', views.VideoDetailView.as_view(), name='video-single'),
    path('audio/', views.PodcastList.as_view(), name='podcasts'),
    path('audio/<slug:slug>', views.PodcastDetailView.as_view(), name='audio-single'),
    path('blog/', views.BlogList.as_view(), name='blog'),
    path('blog/<slug:slug>', views.BlogDetailView.as_view(), name='blog-single'),
    path('blog/<blog_category>/', views.CategoryBlogView.as_view()),
    path('authors', views.BloggerList.as_view(), name='authors'),
    path('authors/<username>', views.BloggerDetailView.as_view(), name='author_profile'),
    path('rss/all/', feeds.RssFeed()),
    path('markdownx/', include(markdownx)),
    path('django-rq/', include('django_rq.urls')),
    path('lntip/', TemplateView.as_view(template_name='lntip.html'))
]

handle404 = 'views.handle404'
