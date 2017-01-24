from oscar.apps.catalogue.views import *
from oscar.apps.catalogue.views import CatalogueView as CoreCatalogueView, ProductCategoryView as CoreProductCategoryView
from oscar.core.loading import get_class, get_model

from django.utils.translation import ugettext_lazy as _

from filter.forms import FilterForm

get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class CatalogueView(CoreCatalogueView):
    def get(self, request, *args, **kwargs):
        self.form = FilterForm(request.GET)
        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), [], options)
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super(CoreCatalogueView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CatalogueView, self).get_context_data(**kwargs)
        ctx['filter_form'] = self.form
        return ctx


class ProductCategoryView(CoreProductCategoryView):
    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        self.category = self.get_category()
        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect

        self.form=FilterForm(request.GET)
        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data

        try:
            self.search_handler = self.get_search_handler(
                request.GET, request.get_full_path(), self.get_categories(), options)
        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())

        return super(CoreProductCategoryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ProductCategoryView, self).get_context_data(**kwargs)
        ctx['filter_form'] = self.form
        return ctx


