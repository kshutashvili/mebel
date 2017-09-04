from django.conf.urls import url, include
from .views import CatalogView #, PopularView


urlpatterns = [
    url(r'^$', CatalogView.as_view(), name='catalogs'),
    # url(r'^popular/', include('apps.catalogs.urls', namespace='catalogs')),
]
