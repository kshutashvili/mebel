from django.conf.urls import url

from apps.promotions.views import ContactView

urlpatterns = [
    url(r'^contacts/', ContactView.as_view(), name='contacts'),
]
