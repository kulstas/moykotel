from django.core.management.base import BaseCommand, CommandError
from moykotel.models import Post, PostCategory


class Command(BaseCommand):
    help = "Удаление новостей из категории"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи из категории {options["category"]}? yes / no: ')

        if answer != "yes":
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
             category = PostCategory.objects.get(name=options['category'])
             Post.objects.filter(category=category).delete()
             self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.category_through}'))
        except Post.DoesNotExist:
             self.stdout.write(self.style.ERROR(f'Could not find category'))
