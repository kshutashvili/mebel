from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

from common.views import AjaxFormMixin

from .models import SiteReview
from .forms import SiteReviewForm

# Create your views here.


class CreateSitetReview(AjaxFormMixin, CreateView):
    template_name = "site_reviews/create.html"
    model = SiteReview
    form_class = SiteReviewForm
    success_url = '/sitereviews/'

    def form_valid(self, form):
        form.save()
        return super(CreateSitetReview, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # check permission to leave review
        if request.user.is_authenticated():
            if request.user.site_reviews.all():
                message = _("You have already reviewed site!")
                messages.warning(self.request, message)

        return super(CreateSitetReview, self).dispatch(request, args, kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateSitetReview, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SiteReviewListView(ListView):
    model = SiteReview
    template_name = 'site_reviews/review_list.html'
    context_object_name = 'reviews_list'

    def get_context_data(self, **kwargs):
        ctx = super(SiteReviewListView, self).get_context_data(**kwargs)
        ctx['review_form'] = SiteReviewForm()
        return ctx