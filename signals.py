from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_rq import enqueue, job
from video_encoding import tasks
from .submodels.media import Video
# from .submodels.people import Blogger
from PIL import Image
from datetime import datetime
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from datetime import datetime
import os, os.path, subprocess, re, glob

@receiver(post_save, sender=Video)
def convert_video(sender, instance, **kwargs):
    enqueue(tasks.convert_all_videos,
        instance._meta.app_label,
        instance._meta.model_name,
        instance.pk)

@receiver(post_save, sender=Video)
def make_thumbnail(sender, instance, **kwargs):
    now = datetime.now()
    directory = settings.MEDIA_ROOT + '/videos/thumbs/{:%Y}'.format(now) + '/{:%m}'.format(now) +'/'
    if not os.path.exists(directory):
        os.makedirs(directory,exist_ok=True)
    video_input_path = settings.MEDIA_ROOT + '/' + instance.file.name
    noex_fn = re.sub('[^A-Za-z0-9]+', '', instance.file.name)
    img_output_path = directory + noex_fn + '.jpg'
    # don't do this if thumb exists - prevents infinite loop
    if not os.path.exists(img_output_path):
        subprocess.check_call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
        thumb_name = noex_fn + '_thumb.jpg'
        pic = Image.open(img_output_path)
        pic.thumbnail((100, 120), Image.ANTIALIAS)

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        pic.save(temp_thumb, 'JPEG')
        temp_thumb.seek(0)

        instance.thumbnail.save(thumb_name, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()
    return True

@receiver(post_delete, sender=Video)
def submission_delete(sender, instance, **kwargs):
    # delete original file and all generated formats. formats first so we have filename
    filename = instance.file.name
    noex = re.sub('[^A-Za-z0-9]+', '', instance.file.name)
    formatdirs = os.path.join(settings.MEDIA_ROOT+'/formats/*/*')
    filelist = glob.glob(formatdirs)
    for f in filelist:
        if noex in f:
            os.remove(f)
    instance.file.delete(False)

