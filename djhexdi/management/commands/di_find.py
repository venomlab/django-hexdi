import hexdi
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from djhexdi import settings
        finder = hexdi.get_finder(settings.HEXDI_FINDER_PACKAGES)
        modules = finder.find()
        self.stdout.write(self.style.SUCCESS(';\n'.join(modules)))
