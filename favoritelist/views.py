from django.shortcuts import render

from django.views.generic import CreateView, FormView, ListView, TemplateView
from .models import FavoriteListLine
# Create your views here.


class FavoriteListCreate(TemplateView):
    template_name = 'favlist/favlist.html'