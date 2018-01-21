import abc
import typing
from hexdi.utils import load_module, get_module_if_exists, load_class
from djhexdi import settings


def load_modules(modules, excluded_modules):
    loader = load_class(settings.HEXDI_LOADER)([m for m in modules if m not in excluded_modules])
    loader.load()


def find_modules(packages):
    finder = load_class(settings.HEXDI_FINDER)(packages)
    return finder.find()


class AbstractStrategy(abc.ABC):
    @abc.abstractmethod
    def go(self): pass


class Dummy(AbstractStrategy):
    def go(self):
        pass


class AbstractLoadModulesStrategy(AbstractStrategy):
    @abc.abstractmethod
    def discover_modules(self) -> typing.List[typing.AnyStr]:
        pass

    def get_excluded_modules(self) -> typing.List[typing.AnyStr]:
        return settings.HEXDI_EXCLUDE_MODULES

    def go(self):
        modules = self.discover_modules()
        excluded = self.get_excluded_modules()
        load_modules(modules, excluded)


class Static(AbstractLoadModulesStrategy):

    def discover_modules(self) -> typing.List[typing.AnyStr]:
        modules = list()
        file = settings.HEXDI_MODULE
        if file and get_module_if_exists(file):
            _module = load_module(file)
            modules.extend(getattr(_module, settings.HEXDI_MODULE_LIST_NAME))
        modules.extend(settings.HEXDI_MODULES_LIST)
        return modules


class Auto(Static):
    def discover_modules(self) -> typing.List[typing.AnyStr]:
        packages = settings.HEXDI_FINDER_PACKAGES
        modules = find_modules(packages)
        static_modules = super(Auto, self).discover_modules()
        modules.extend(static_modules)
        return modules
