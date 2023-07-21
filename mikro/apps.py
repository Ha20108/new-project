from django.apps import AppConfig


class MikroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mikro'
    def ready(self):
        try:
            import mikro.templatetags.blog_tags
        except ImportError:
            pass

