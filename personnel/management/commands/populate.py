from optparse import make_option

from django.core.management import call_command
from django.core.management.base import BaseCommand
from population_script import run_population


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--flush', action="store_true", dest="flush_db", default=False,
                    help="Will flush the database before running the population script"),
    )

    def handle(self, *args, **options):
        if options.get("flush_db"):
            call_command('flush', interactive=True)
            call_command('createsuperuser', interactive=True)
        run_population()
