from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Article
# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/all_articles.html'
    context_object_name = 'articles_list'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
