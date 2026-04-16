from django.apps import AppConfig


class NewsappConfig(AppConfig):
    name = 'newsapp'
    verbose_name ='Newws'

    def ready(self):
        import newsapp.signals

    
