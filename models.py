from django.db import models
from .submodels.media import Pic, Video, Promo, Podcast # TODO: Add audio model/field
from .submodels.taxonomy import Category
from .submodels.people import Blogger
from markdownx.models import MarkdownxField

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = MarkdownxField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(Blogger, null=True, on_delete=models.CASCADE)
    blogimg = models.ForeignKey(Pic, blank=True, null=True, on_delete=models.SET_NULL)
    blogvid = models.ForeignKey(Video, blank=True, null=True, on_delete=models.PROTECT)
    blogaudio = models.ForeignKey(Podcast, blank=True, null=True, on_delete=models.PROTECT)    
    promos = models.ManyToManyField(Promo, blank=True)
    
    class Meta:
        ordering = ['-posted']
        db_table = 'blog_blog'
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('view_blog_category', None, { 'slug': self.slug })



