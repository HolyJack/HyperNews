from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from datetime import datetime
import re
import json


def get_json():
    with open(settings.NEWS_JSON_PATH) as f:
        news_json = json.load(f)
    return news_json


def save_json(news_json):
    with open(settings.NEWS_JSON_PATH, 'w') as f:
        json.dump(news_json, f)


def get_new_id():
    news_json = get_json()
    max_link = max(news_json, key=lambda news: news['link'])['link']
    return max_link + 1


def save_new_article(new_article):
    news_json = get_json()
    news_json.append(new_article)
    save_json(news_json)


def get_context(link):
    news_json = get_json()

    if news_json is not None:
        for article in news_json:
            if article['link'] == link:
                return article

    return None


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class ArticleView(View):
    template_name = 'article.html'

    def get(self, request, *args, **kwargs):
        link = self.kwargs['link']
        context = get_context(link)
        return render(request, f'news/{self.template_name}', context=context)


class NewsView(View):
    template_name = 'news.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        news_json = get_json()
        if q is not None:
            news_json = [x for x in news_json if q.lower() in x['title'].lower()]
        context = {"news": news_json}
        return render(request, f'news/{self.template_name}', context=context)


class CreateView(View):
    template_name = 'create.html'

    def get(self, request, *args, **kwargs):
        return render(request, f'news/{self.template_name}')

    def post(self, request, *args, **kwargs):
        new_article = dict()
        new_article['title'] = request.POST['title']
        new_article['text'] = request.POST['text']
        new_article['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_article['link'] = get_new_id()
        save_new_article(new_article)
        return redirect('/news/')
