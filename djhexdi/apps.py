from hexdi.utils import load_class
from django.apps import AppConfig


class DjhexdiConfig(AppConfig):
    name = 'hexdi'

    def ready(self):
        from djhexdi import settings
        strategy = load_class(settings.HEXDI_STRATEGY)()
        strategy.go()
