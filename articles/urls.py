from django.conf.urls import url

from articles.views import ArticleListView

urlpatterns = [
    url(r'^$', ArticleListView.as_view(), name='all'),
]
