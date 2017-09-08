from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from oscar.apps.promotions.views import HomeView as DefaultHomeView

from oscar.core.loading import get_model

from slider.models import SliderSlide

Product = get_model('catalogue', 'Product')
StockRecord = get_model('partner', 'StockRecord')


class HomeView(DefaultHomeView):
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['discounted_products'] = StockRecord.objects.filter(product__discount_type__isnull=False)
        last_products = Product.browsable.base_queryset()
        paginator = Paginator(last_products, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            last_products = paginator.page(page)
        except PageNotAnInteger:
            last_products = paginator.page(1)
        except EmptyPage:
            last_products = paginator.page(paginator.num_pages)
        context['last_products'] = last_products
        context['slides'] = SliderSlide.objects.all()
        return context
