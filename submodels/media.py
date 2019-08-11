from django.db import models
import os.path
from pathlib import Path
from datetime import datetime
from .taxonomy import Category
from .people import Blogger
from PIL import Image
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.contenttypes.fields import GenericRelation
from video_encoding.fields import VideoField
from video_encoding.models import Format
from audiofield.fields import AudioField
import os, os.path
from markdownx.models import MarkdownxField

# general purpose media types

class Pic(models.Model):
    title = models.CharField(max_length=99)
    desc = models.TextField(max_length=300)
    posted =models.DateField(db_index=True, auto_now_add=True)
    pic = models.ImageField(upload_to='blogimg/%Y/%m/%d')
    thumbnail = models.ImageField(upload_to='thumbs/%Y/%m/', editable=False)
    displaypic = models.ImageField(upload_to='blogimg/display/%Y/%m/%d', null=True, editable=False)

    class Meta:
        db_table="blog_pic"

    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            thumbnail = 'thumbs/default.jpg'
            raise Exception('Could not create thumbnail - is the file type valid?')

        basewidth=600
        pic = Image.open(self.pic)
        wpercent = (basewidth / float(pic.size[0]))
        hsize = int((float(pic.size[1]) * float(wpercent)))
        pic = pic.resize((basewidth, hsize), Image.ANTIALIAS)
        super(Pic, self).save(*args, **kwargs)
 
    def make_thumbnail(self):

        pic = Image.open(self.pic)
        pic.thumbnail((100, 120), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.pic.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        pic.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

class Promo(models.Model):
    title = models.CharField(max_length=100)
    body = MarkdownxField()
    link_to = models.CharField(max_length=270, null=True, blank=True)
    adimg = models.ForeignKey(Pic, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table="blog_promo"

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    creator = models.ForeignKey(Blogger, null = True, on_delete= models.CASCADE)
    description = models.TextField(max_length=1000)
    posted = models.DateField(db_index=True, auto_now_add=True)
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    duration = models.FloatField(editable=False, null=True)
    file = VideoField(width_field='width', height_field='height', duration_field='duration')
    category=models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    format_set=GenericRelation(Format)
    thumbnail = models.ImageField(upload_to='videos/thumbs/%Y/%m/', editable=False, null=True)
    promos = models.ManyToManyField(Promo, blank=True)

    class Meta:
        db_table = "blog_video"
    
    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('videos', None, { 'slug': self.slug })

    def file_name(self):
        # Remove extension so we can serve the right file per browser
        sep = '.'
        return self.file.name.split(sep, 1)[0]
    
class Podcast(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    creator = models.ForeignKey(Blogger, null = True, on_delete= models.CASCADE)
    description = models.TextField(max_length=1000)
    itunes_explicit = models.BooleanField(default=True)
    pubdate = models.DateField(db_index=True, auto_now_add=True)
    pic = models.ForeignKey(Pic, blank=True, null=True, on_delete=models.SET_NULL)    
    audio_file = AudioField(ext_whitelist=(".mp3", ".wav", ".ogg"), help_text=("Allowed type - .mp3, .wav, .ogg"))
    promos = models.ManyToManyField(Promo, blank=True)
    class Meta:
        db_table="blog_podcast"
    
    def __str__(self):
        return self.title
    
    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')
 
