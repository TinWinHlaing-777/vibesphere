from django.contrib import admin
from .models import BlogPage, Article, Comment

admin.site.register(BlogPage)
admin.site.register(Article)
admin.site.register(Comment)

