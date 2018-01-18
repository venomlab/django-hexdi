import os
import hexdi
from django.core.management import BaseCommand
from djhexdi import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f',
                            dest='filename',
                            metavar='filename',
                            default=settings.HEXDI_MODULE,
                            type=str,
                            help='filename to store finder results')
        parser.add_argument('--auto',
                            const=True,
                            default=False,
                            nargs='?',
                            metavar='',
                            help='automatically create packages for module')

    def handle(self, *args, **options):
        finder = hexdi.get_finder(settings.HEXDI_FINDER_PACKAGES)
        modules = finder.find()
        modules_text = "{} = [\n{}\n]".format(
            settings.HEXDI_MODULES_LIST_NAME,
            ",\n".join(["    \'{}\'".format(m) for m in modules])
        )
        raw_module_name = options['filename']
        if raw_module_name:
            filename = self.__sanitinze_hexdi_module_name(raw_module_name)
            self.__check_dir_exists_for_module(filename, options['auto'])
            with open(filename, 'w', encoding='utf8') as file:
                file.write(modules_text)
        else:
            self.stdout.write(modules_text)

    def __check_dir_exists_for_module(self, filename, auto_create):
        path, modulename = filename.rsplit('/', 1)
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
