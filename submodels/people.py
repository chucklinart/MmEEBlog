from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from markdownx.models import MarkdownxField
from PIL import Image

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blogger")
    bio = MarkdownxField(max_length=500, blank=True)
    profile_image = models.ImageField(
        upload_to='blogimg/profiles/',
        null=True,
        blank=True,
        help_text="User Headshot",
    )
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=True, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=True, default="100")

    class Meta:
      db_table = "blog_blogger"

    def __str__(self):
        return self.user.username
   
    def has_user(self):
        return self.user.user_id is not None
    
    def save(self, *args, **kwargs):
        if not self.profile_image:
            return
        super(Blogger, self).save(*args, **kwargs)
        profile_image = Image.open(self.profile_image)
        (width, height) = profile_image.size
        size = ( 100, 100)
        profile_image = profile_image.resize(size, Image.ANTIALIAS)
        profile_image.save(self.profile_image.path)

