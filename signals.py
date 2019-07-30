from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_rq import enqueue, job
from video_encoding import tasks
from .submodels.media import Video
from .submodels.people import Blogger
import os, os.path, glob

@receiver(post_save, sender=Video)
def convert_video(sender, instance, **kwargs):
    enqueue(tasks.convert_all_videos,
        instance._meta.app_label,
        instance._meta.model_name,
        instance.pk)

@receiver(post_delete, sender=Video)
def submission_delete(sender, instance, **kwargs):
    # delete original file and all generated formats
    instance.file.delete(False)
    # TODO: delete formatted files
    formatdir = os.path.join(settings.MEDIA_ROOT+'/formats/')
    filelist = glob.glob(os.path.join(formatdir, '*'+filename+'.*'))
    for f in filelist:
        os.remove(f)
    
    
'''
@receiver(post_save, sender=User)
def create_user_blogger(sender, instance, created, **kwargs):
    if created:
        person = Blogger()
        person.user = instance
        save(person)

@receiver(post_save, sender=User)
def save_user_blogger(sender, instance, **kwargs):
    if instance.blogger:
        instance.blogger.save(user=instance)
    else: 
        Blogger.objects.create(user=instance, bio="Add Bio")
'''
