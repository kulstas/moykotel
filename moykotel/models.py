from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_avatar = models.ImageField(default='default.jpg', upload_to='img/users/')
    user_phone = models.CharField(max_length=10, default="+7000000000")

    admin = 'AD'
    manager = 'MG'
    service = 'SV'
    client = 'CL'

    POSITIONS = [
        (admin, 'Администратор'),
        (manager, 'Контентв-менеджер'),
        (service, 'Сервисный центр'),
        (client, 'Заказчик')
    ]

    user_role = models.CharField(max_length=2,
                                 choices=POSITIONS,
                                 default=client)


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    # обновляет рейтинг текущего автора
    def update_rating(self):
        post_update, comment_update = 0, 0

        post_rate = self.post_set.aggregate(post_rate_sum=Sum('post_rating'))
        post_update += post_rate.get('post_rate_sum')
        comment_rate = self.author_user.comment_set.aggregate(comment_rate_sum=Sum('comment_rating'))
        comment_update += comment_rate.get('comment_rate_sum')

        self.author_rating = post_update * 3 + comment_update
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    post_author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE
    )

    post_category = models.ManyToManyField(
        Category,
        through='PostCategory',
        related_name='posts'
    )

    post_title = models.CharField(
        max_length=56,
        db_index=True,
        unique=True
    )

    post_text = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    post_rating = models.SmallIntegerField(default=0)

    ARTICLE = 'AR'
    NEWS = 'NW'

    CATEGORY_TYPES = [
        (ARTICLE, "Статья"),
        (NEWS, "Новость")
    ]

    post_type = models.CharField(max_length=2, choices=CATEGORY_TYPES, default=ARTICLE)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    # возвращает начало статьи
    def preview(self):
        return self.post_text[0:124] + "..."

    # формат вывода объекта на фронтенде
    def __str__(self):
        return f'{self.post_title.title()}: {self.post_text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()




