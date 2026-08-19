from django.shortcuts import render, get_object_or_404
from .models import News

def detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'news/news_details.html', {'item': news_item})

def news_list(request):
    return render(request, 'news/all_news.html', {'news': News.objects.filter(is_published=True)})