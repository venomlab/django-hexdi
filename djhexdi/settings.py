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

from django.conf import settings

HEXDI_STRATEGY = getattr(settings, 'HEXDI_STRATEGY', 'djhexdi.strategy.Dummy')
HEXDI_FINDER_PACKAGES = getattr(settings, 'HEXDI_FINDER_PACKAGES', settings.INSTALLED_APPS)
HEXDI_MODULES_LIST = getattr(settings, 'HEXDI_MODULES_LIST', [])
HEXDI_EXCLUDE_MODULES = getattr(settings, 'HEXDI_EXCLUDE_MODULES', [])
HEXDI_MODULE_LIST_NAME = getattr(settings, 'HEXDI_MODULE_LIST_NAME', 'HEXDI_MODULES_LIST')
HEXDI_MODULE = getattr(settings, 'HEXDI_MODULE', None)
HEXDI_LOADER = getattr(settings, 'HEXDI_LOADER', 'hexdi.loader.BasicLoader')
HEXDI_FINDER = getattr(settings, 'HEXDI_LOADER', 'hexdi.finder.RecursiveRegexFinder')
