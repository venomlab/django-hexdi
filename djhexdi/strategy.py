#    Highly extensible Dependency injection framework for humans. Django integration
#    Copyright (C) 2017 Dmitriy Selischev
#    The MIT License (MIT)
#    
#    Permission is hereby granted, free of charge, to any person obtaining
#    a copy of this software and associated documentation files
#    (the "Software"), to deal in the Software without restriction,
#    including without limitation the rights to use, copy, modify, merge,
#    publish, distribute, sublicense, and/or sell copies of the Software,
#    and to permit persons to whom the Software is furnished to do so,
#    subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
