from django.conf.urls import include, url

from oscar.apps.catalogue.reviews.app import application as reviews_app
from oscar.core.application import Application
from oscar.core.loading import get_class

from .views import AddProductToFavorite, RemoveProductFromFavorite, OneClickOrderCreateView


class BaseCatalogueApplication(Application):
    name = 'catalogue'
    detail_view = get_class('catalogue.views', 'ProductDetailView')
    catalogue_view = get_class('catalogue.views', 'CatalogueView')
    category_view = get_class('catalogue.views', 'ProductCategoryView')
    range_view = get_class('offer.views', 'RangeDetailView')

    def get_urls(self):
        urlpatterns = super(BaseCatalogueApplication, self).get_urls()
        urlpatterns += [
            url(r'^$', self.catalogue_view.as_view(), name='index'),
            url(r'^(?P<category_slug>[\w-]+(/[\w-]+)*)_*(?P<id>\d*)/(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
            url(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/addtofav/$',
                AddProductToFavorite, name='add_to_fav'),
            url(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/rmfromfav/$',
                RemoveProductFromFavorite, name='rm_from_fav'),
            url(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/oneclick/$',
                OneClickOrderCreateView.as_view(), name='oneclick'),
            url(r'^(?P<category_slug>[\w-]+(/[\w-]+)*)_(?P<pk>\d+)/$',
                self.category_view.as_view(), name='category'),
            # Fallback URL if a user chops of the last part of the URL
            url(r'^(?P<category_slug>[\w-]+(/[\w-]+)*)/$',
                self.category_view.as_view()),
            url(r'^ranges/(?P<slug>[\w-]+)/$',
                self.range_view.as_view(), name='range')]
        return self.post_process_urls(urlpatterns)


class ReviewsApplication(Application):
    name = None
    reviews_app = reviews_app

    def get_urls(self):
        urlpatterns = super(ReviewsApplication, self).get_urls()
        urlpatterns += [
            url(r'^(?P<product_slug>[\w-]*)_(?P<product_pk>\d+)/reviews/',
                include(self.reviews_app.urls)),
        ]
        return self.post_process_urls(urlpatterns)


class CatalogueApplication(BaseCatalogueApplication, ReviewsApplication):
    """
    Composite class combining Products with Reviews
    """


application = CatalogueApplication()
