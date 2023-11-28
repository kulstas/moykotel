"""
URL configuration for moykotel moykotel.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import views
from .views import (PostsList, PostDetail, PostsSearch, PostCreate, PostUpdate, PostDelete, NewsList, NewsCreate, subscriptions
)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('pages/', include("django.contrib.flatpages.urls")),
    path('oshibki-kotlov/', PostsList.as_view(), name='posts_list'),
    path('oshibki-kotlov/<int:id>', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('oshibki-kotlov/search/', PostsSearch.as_view(), name='posts_search'),
    path('oshibki-kotlov/create/', PostCreate.as_view(), name='post_create'),
    path('oshibki-kotlov/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('oshibki-kotlov/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:id>', PostDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('subscriptions/', subscriptions, name="subscriptions"),
]