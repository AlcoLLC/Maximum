from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    all_news = News.objects.filter(is_active=True)
    top_news = News.objects.filter(is_top=True).first()

    context = {
        'all_news': all_news,
        'top_news': top_news,
    }
    
    return render(request, 'news.html', context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    contents = news.contents.all()
    
    context = {
        'news': news,
        'contents': contents,
    }
    return render(request, 'news_detail.html', context)
