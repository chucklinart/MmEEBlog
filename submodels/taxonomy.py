from django.db import models

# general purpose top-level Categories
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(max_length=280)
    class Meta:
        verbose_name_plural = "categories"
    def __unicode__(self):
        return '%s' % self.title
    def __str__(self):
        return self.title

