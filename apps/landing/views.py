from django.shortcuts import render
from apps.news.models import News
from apps.catalog.models import Category

def main(request):
    news = News.objects.filter(is_published=True)[:5]
    categories = Category.objects.all()
    return render(request, 'landing/main.html', {
        'news': news,
        'categories': categories,
    })

def about(request):
    return render(request, 'landing/about.html')

def contact(request):
    return render(request, 'landing/contact.html')
