from oscar.apps.catalogue.search_handlers import *
from oscar.apps.catalogue.search_handlers import SimpleProductSearchHandler as CoreSimpleProductSearchHandler

from django.db.models import Q


class SimpleProductSearchHandler(CoreSimpleProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None, options=[]):
        self.options = options
        super(SimpleProductSearchHandler, self).__init__(request_data, full_path, categories)

    def get_queryset(self):

        qs = Product.browsable.base_queryset()
        if self.categories:
            qs = qs.filter(categories__in=self.categories).distinct()

        print(self.options)
        if self.options:
            for k in self.options:
                if k.startswith('filter_') and self.options[k]:
                    code = k.replace('filter_', '')
                    qs = qs.filter(
                        Q(multiple_options__group__code=code),
                        reduce(lambda x, y: x | y,
                               [Q(multiple_options__choices__variant__pk=item) for item in self.options[k]]
                               )
                    ).distinct()
        return qs


