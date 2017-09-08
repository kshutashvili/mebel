# -*- coding: utf-8 -*-

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from oscar.apps.promotions.models import HandPickedProductList

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
        try:
            context['popular'] = HandPickedProductList.objects.get(name=u'Популярное').get_products()
        except HandPickedProductList.DoesNotExist:
            pass

        try:
            context['recommended'] = HandPickedProductList.objects.get(name=u'Рекомендуемое').get_products()
        except HandPickedProductList.DoesNotExist:
            pass

        context['slides'] = SliderSlide.objects.all()
        return context
