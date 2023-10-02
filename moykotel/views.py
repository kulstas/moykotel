from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datetime import datetime

from .models import Post, Comment
from .forms import PostForm
from .filters import PostsFilter

"""Функция отображения главной страницы"""
def index(request):
    return render(
        request,
        'index.html'
    )


class PostsList(ListView):
    model = Post
    ordering = 'post_title'

    # Имя шаблона
    template_name = 'posts.html'

    # Зависит от регистра.
    context_object_name = 'posts'

    # Пагинация
    paginate_by = 6

    # переопределяем метод дженерика
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context

    # Использование фильтра по цене (пример)
    # queryset = Post.objects.filter(
    #     price__lt=300
    # ).order_by(
    #     'post_title'
    # )

class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class CommentsPost(ListView):
    model = Comment
    ordering = 'comment_date'
    template_name = 'post.html'
    context_object_name = 'comments'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

class NewsList(ListView):
    model = Post
    ordering = 'post_date'
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type__contains='NW')  # отфильтровываем новости
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        return super().form_valid(form)