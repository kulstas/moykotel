from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', '_preview', '_category', 'post_date')
    list_filter = ('post_category',)
    search_fields = ('post_title',)


    def _category(self, row):
        return ', '.join([x.category_name for x in row.post_category.all()])

    def _preview(self, row):
        return row.post_text[0:164] + "..."


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', '_posts')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)