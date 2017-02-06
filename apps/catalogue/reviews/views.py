from oscar.apps.catalogue.reviews.views import *
from .forms import ProductReviewForm

from django.http import HttpResponse

from common.views import AjaxFormMixin
from apps.catalogue.models import Product

class CreateProductReview(AjaxFormMixin):
    form_class = ProductReviewForm
    product_model = Product

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.title = ' '
        instance.save()
        return HttpResponse(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            self.product_model, pk=kwargs['product_pk'])
        # check permission to leave review

        return super(CreateProductReview, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateProductReview, self).get_form_kwargs()
        kwargs['product'] = self.product
        if self.request.user.is_authenticated():
            kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return self.product.get_absolute_url()