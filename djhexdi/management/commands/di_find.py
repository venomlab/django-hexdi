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

import os
import hexdi
from django.core.management import BaseCommand
from djhexdi import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-m',
                            dest='modulepath',
                            metavar='modulepath',
                            default=settings.HEXDI_MODULE,
                            type=str,
                            help='Optional. Dotted path to module that stores finder results.\n' +
                                 'Used HEXDI_MODULE({}) setting by default.'.format(settings.HEXDI_MODULE))
        parser.add_argument('--auto',
                            const=True,
                            default=False,
                            nargs='?',
                            metavar='',
                            help='Optional. Automatically create packages tree for module.')

    def handle(self, *args, **options):
        finder = hexdi.get_finder(settings.HEXDI_FINDER_PACKAGES)
        modules = finder.find()
        modules_text = "{} = [\n{}\n]".format(
            settings.HEXDI_MODULE_LIST_NAME,
            ",\n".join(["    \'{}\'".format(m) for m in modules])
        )
        raw_module_name = options['modulepath']
        if raw_module_name:
            filename = self.__sanitinze_hexdi_module_name(raw_module_name)
            self.__check_dir_exists_for_module(filename, options['auto'])
            with open(filename, 'w', encoding='utf8') as file:
                file.write(modules_text)
        else:
            self.stdout.write(modules_text)

    def __check_dir_exists_for_module(self, filename, auto_create):
        if '/' in filename:
            path, module_name = filename.rsplit('/', 1)
        else:
            path = ''
        path_parts = path.split('/')
        path_acc = ''
        for part in path_parts:
            path_acc += "{}/".format(part)
            if not os.path.isdir(path_acc):
                if auto_create:
                    os.mkdir(path_acc)
                    init_module_path = "{}__init__.py".format(path_acc)
                    with open(init_module_path, 'w', encoding='utf8'):
                        pass
                else:
                    raise Exception("No such path: {}".format(path))

    def __sanitinze_hexdi_module_name(self, name: str):
        if not name.endswith('.py'):
            _path = name.replace('.', '/')
        else:
            _path, _py = name.rsplit('.', 1)
            _path = _path.replace('.', '/')
        return "{}.py".format(_path)
