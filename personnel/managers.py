import operator
from django.db import models
from django.db.models import Q


class DefaultManager(models.Manager):

    def search(self, search_terms, model='Cadet'):
        terms = [term.strip() for term in search_terms.split()]
        q_objects = []

        if model == 'Cadet':
            for term in terms:
                q_objects.append(Q(user__first_name__icontains=term))
                q_objects.append(Q(user__last_name__icontains=term))
        elif model is 'Company':
            for term in terms:
                q_objects.append(Q(name__icontains=term))
        elif model is 'MS':
            for term in terms:
                q_objects.append(Q(name__icontains=term))

        # Start with a bare QuerySet
        qs = self.get_queryset()

        # Use operator's or_ to string together all of your Q objects.
        return qs.filter(reduce(operator.or_, q_objects))


class CadetManager(DefaultManager):

    def get_queryset(self):
        query = super(CadetManager, self).get_queryset()
        return query.filter(approved=True)

    def get_unapproved(self):
        query = super(CadetManager, self).get_queryset()
        return query.filter(approved=False)