from django.conf.urls import url, include
from .views import CatalogView


urlpatterns = [
    url(r'^$', CatalogView.as_view(), name='catalogs'),
]
