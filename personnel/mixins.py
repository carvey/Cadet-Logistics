from abc import ABCMeta, abstractmethod
from django.db.models.base import ModelBase
from django.utils import six

# class GroupingMeta(ModelBase, ABCMeta): pass

# six.add_metaclass()

@six.add_metaclass(ModelBase)
class GroupingMixin():
    """
    This class defines some methods that all grouping models should override, as well as a helper function
     that all numbered groupings can use. This class can be used to properly abstract the grouping pages.
    A mixin is used here instead of a parent class so that abstract methods can be enfored in subclasses
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def short_name(self):
        pass

    @abstractmethod
    def get_sub_groupings(self):
        pass

    def get_sub_cadets(self):
        return self.cadets.all()

    @abstractmethod
    def get_link(self):
        pass

    @abstractmethod
    def get_co(self):
        pass

    @abstractmethod
    def get_sgt(self):
        pass

    def number_end_str(self):
        """
        Should return a number ending string for groupings that are numbered (squad and platoon)
        :param grouping: the grouping to get the ending string for
        :return: the ending string
        """
        if hasattr(self, 'number'):
            end_string = "th"
            if self.number % 10 == 1:
                end_string = "st"
            elif self.number % 10 == 2:
                end_string = "nd"
            elif self.number % 10 == 3:
                end_string = "rd"

            return end_string


