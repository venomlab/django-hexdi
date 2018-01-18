import hexdi
from djhexdi import settings
from hexdi.utils import load_module


class AbstractStrategy:
    def go(self):
        pass


class Dummy(AbstractStrategy):
    pass


class Static(AbstractStrategy):
    def _load_modules(self, modules):
        loader = hexdi.get_loader([m for m in modules if m not in settings.HEXDI_EXCLUDE_MODULES])
        loader.load()

    def go(self):
        modules = list()
        modules.extend(settings.HEXDI_MODULES_LIST or [])
        file = settings.HEXDI_MODULE
        if file:
            _module = load_module(file)
            modules.extend(getattr(_module, settings.HEXDI_MODULES_LIST_NAME))
        self._load_modules(modules)


class Auto(Static):
    def go(self):
        packages = settings.HEXDI_FINDER_PACKAGES
        finder = hexdi.get_finder(packages)
        modules = finder.find()
        self._load_modules(modules)
