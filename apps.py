from django.apps import AppConfig


class MmeeBlogConfig(AppConfig):
    name = 'mmeeblog'

    def ready(self):
        import mmeeblog.signals
