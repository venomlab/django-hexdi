from django.conf import settings

HEXDI_STRATEGY = getattr(settings, 'HEXDI_STRATEGY', 'djhexdi.strategy.Dummy')
HEXDI_FINDER_PACKAGES = getattr(settings, 'HEXDI_FINDER_PACKAGES', settings.INSTALLED_APPS)
HEXDI_MODULES_LIST = getattr(settings, 'HEXDI_MODULES_LIST', [])
HEXDI_EXCLUDE_MODULES = getattr(settings, 'HEXDI_EXCLUDE_MODULES', [])
HEXDI_MODULE_LIST_NAME = getattr(settings, 'HEXDI_MODULE_LIST_NAME', 'HEXDI_MODULES_LIST')
HEXDI_MODULE = getattr(settings, 'HEXDI_MODULE', None)
HEXDI_LOADER = getattr(settings, 'HEXDI_LOADER', 'hexdi.loader.BasicLoader')
HEXDI_FINDER = getattr(settings, 'HEXDI_LOADER', 'hexdi.finder.RecursiveRegexFinder')
