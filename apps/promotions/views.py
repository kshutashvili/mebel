from django.views.generic import TemplateView

from oscar.apps.promotions.views import HomeView as DefaultHomeView

from oscar.core.loading import get_model

from slider.models import SliderSlide

Product = get_model('catalogue', 'Product')


class HomeView(DefaultHomeView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['last_products'] = Product.browsable.base_queryset()[:9]
        context['slides'] = SliderSlide.objects.all()
        return context


class ContactView(TemplateView):
    template_name = 'promotions/contacts.html'
