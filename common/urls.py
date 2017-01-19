from django.conf.urls import url

from common import views

urlpatterns = [
    url(r'^contacts/$', views.ContactsView.as_view(), name='contacts'),
    url(r'^send/message/$', views.MessageView.as_view(), name='send_message'),
]
