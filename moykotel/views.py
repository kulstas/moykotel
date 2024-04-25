from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.translation import gettext as _

from datetime import datetime

from .models import Post, Category, Comment, Subscriber
from .forms import PostForm, CommentForm
from .filters import PostsFilter


"""Функция отображения главной страницы"""
@cache_page(60)
def index(request):
    return render(
        request,
        'moykotel/index.html'
    )


class PostsList(ListView):
    model = Post
    ordering = 'post_title'

    # Имя шаблона
    template_name = 'moykotel/posts.html'

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
    template_name = 'moykotel/search.html'
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


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'moykotel/post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'
    form_class = CommentForm
    queryset = Post.objects.all()

    def get_success_url(self):
        return reverse_lazy(kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.comment_post = self.get_object()
        self.object.comment_user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_object(self, *args, **kwargs):
        obj = cache.get(self.kwargs["id"], None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(self.kwargs["id"], obj)

        return obj


class CommentsPost(DetailView):
    model = Comment
    ordering = 'comment_date'
    template_name = 'moykotel/post.html'
    context_object_name = 'comments'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('moykotel.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'moykotel/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('moykotel.change_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'moykotel/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('moykotel.delete_post')
    raise_exception = True
    model = Post
    template_name = 'moykotel/post_delete.html'
    success_url = reverse_lazy('posts_list')


class NewsList(ListView):
    model = Post
    ordering = 'post_date'
    template_name = 'moykotel/news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type__contains='NW')  # отфильтровываем новости
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('moykotel.add_news')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'moykotel/post_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        return super().form_valid(form)


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(
                user=request.user,
                category=category
            )
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category_name')

    return render(
        request,
        'moykotel/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )