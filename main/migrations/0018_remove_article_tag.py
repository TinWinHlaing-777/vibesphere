# Generated by Django 4.2.15 on 2024-09-02 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_article_published_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tag',
        ),
    ]
