from django.views.generic import ListView

from .models import Catalog, Popular


class CatalogView(ListView):
    template_name = 'catalogs/catalogs.html'
    context_object_name = 'catalogs'

    def get_queryset(self):
        return Catalog.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)
        context['populars'] = Popular.objects.all()
        return context
