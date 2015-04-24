from optparse import make_option

from django.core.management.base import BaseCommand
from pt.models import Grader
from pt.pt_utils.utils import create_graders

class Command(BaseCommand):
    """
    This is a utility command meant to update all the grader objects once the constants.py file has been updated
    """

    def handle(self, *args, **options):
        Grader.objects.all().delete()
        create_graders()
