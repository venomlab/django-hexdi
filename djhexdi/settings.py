from django.conf import settings

HEXDI_STRATEGY = getattr(settings, 'HEXDI_STRATEGY', 'djhexdi.strategy.Dummy')
HEXDI_FINDER_PACKAGES = getattr(settings, 'HEXDI_FINDER_PACKAGES', settings.INSTALLED_APPS)
HEXDI_MODULES_LIST_NAME = getattr(settings, 'HEXDI_MODULE_LIST_NAME', 'HEXDI_MODULES_LIST')
HEXDI_MODULES_LIST = getattr(settings, HEXDI_MODULES_LIST_NAME, None)
HEXDI_EXCLUDE_MODULES = getattr(settings, 'HEXDI_EXCLUDE_MODULES', [])
HEXDI_MODULE = getattr(settings, 'HEXDI_MODULE', None)
