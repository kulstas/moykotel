# Generated by Django 4.2.5 on 2024-04-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moykotel", "0009_alter_subscriber_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="category_name_en_us",
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="category",
            name="category_name_ru",
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="post",
            name="post_title_en_us",
            field=models.CharField(
                db_index=True, max_length=56, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="post_title_ru",
            field=models.CharField(
                db_index=True, max_length=56, null=True, unique=True
            ),
        ),
    ]
