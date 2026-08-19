from django.shortcuts import render
from .models import News

def detail(request, slug):
    pass

def news_list(request):
    return render(request, 'news/all_news.html', {'news': News.objects.filter(is_published=True)})