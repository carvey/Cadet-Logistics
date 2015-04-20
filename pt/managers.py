import datetime
# from pytz import timezone
from django.db import models
# from django.conf import settings

# tz = timezone(settings.TIME_ZONE)


class FilteredTestManager(models.Manager):

    def get_queryset(self):
        """
        Filters out tests from the manager that don't have any scores associated with them yet
        :return: queryset absent of pt tests that don't have any scores
        :return type: Queryset
        """
        query = super(FilteredTestManager, self).get_queryset()
        today = datetime.date.today()
        query = query.filter(date__lte=today)
        return query


class FutureTestManager(models.Manager):

    def get_queryset(self):
        query = super(FutureTestManager, self).get_queryset()
        today = datetime.date.today()
        query = query.filter(date__gte=today)
        return query