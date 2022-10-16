from django.urls import path
from .views import IndexView, ArticleView, NewsView, CreateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view()),
    path('news/', NewsView.as_view()),
    path('news/<int:link>/', ArticleView.as_view()),
    path('news/create/', CreateView.as_view()),
]

urlpatterns += static(settings.STATIC_URL)
