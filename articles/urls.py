from django.conf.urls import url

from articles.views import ArticleListView, ArticleDetailView

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='all'),
    url(r'^(?P<pk>[\d]+)', ArticleDetailView.as_view(), name='detail')
]
