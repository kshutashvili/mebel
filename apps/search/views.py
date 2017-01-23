from oscar.apps.search.views import FacetedSearchView as CoreFacetedSearchView


class FacetedSearchView(CoreFacetedSearchView):
    def get_results(self):
        sqs = super(FacetedSearchView, self).get_results()
        return sqs