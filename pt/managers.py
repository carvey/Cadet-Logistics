from django.db import models

class FilteredTestManager(models.Manager):

    def get_queryset(self):
        """
        Filters out tests from the manager that don't have any scores associated with them yet
        :return: queryset absent of pt tests that don't have any scores
        :return type: Queryset
        """
        query = super(FilteredTestManager, self).get_queryset()
        score_set = [x.id for x in query if x.ptscore_set.all()]
        query = query.filter(id__in=score_set)
        return query


class FutureTestManager(models.Manager):

    def get_queryset(self):

        query = super(FutureTestManager, self).get_queryset()
        score_set = [x.id for x in query if x.ptscore_set.all()]
        query = query.exclude(id__in=score_set)
        return query