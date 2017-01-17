from oscar.apps.catalogue.reviews.abstract_models import AbstractProductReview

from django.utils.translation import ugettext_lazy as _


class ProductReview(AbstractProductReview):

    @property
    def reviewer_name(self):
        if self.user:
            name = self.user.username
            return name if name else _('anonymous')
        else:
            return self.name

from oscar.apps.catalogue.reviews.models import *
