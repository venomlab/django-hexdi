import hexdi
from django.core.management import BaseCommand
from djhexdi.utils import sanitinze_hexdi_module_name
from djhexdi import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f',
                            metavar='filename',
                            default=settings.HEXDI_MODULE,
                            type=str,
                            help='filename to store finder results')

    def handle(self, *args, **options):
        finder = hexdi.get_finder(settings.HEXDI_FINDER_PACKAGES)
        modules = finder.find()
        modules_text = "{} = [\n{}\n]".format(
            settings.HEXDI_MODULES_LIST_NAME,
            ",\n".join(["    \'{}\'".format(m) for m in modules])
        )
        raw_module_name = options['f']
        if raw_module_name:
            filename = sanitinze_hexdi_module_name(raw_module_name)
            with open(filename, 'w', encoding='utf8') as file:
                file.write(modules_text)
        else:
            self.stdout.write(modules_text)
