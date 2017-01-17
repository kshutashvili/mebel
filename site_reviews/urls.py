from django.conf.urls import url

from site_reviews.views import CreateSitetReview, SiteReviewListView

urlpatterns = [
    url(r'^$', SiteReviewListView.as_view(), name='reviews_list'),
    url(r'^create_review/$', CreateSitetReview.as_view(), name='create'),
]
