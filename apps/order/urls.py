from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^create_order/$', SimpleOrderView.as_view(), name='create_order')
]