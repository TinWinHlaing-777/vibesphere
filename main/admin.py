from django.contrib import admin
from .models import User, Article

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'nick_name', 'phone_number', 'nationality', 'country', 'city', 'postal_code', 'created_date', 'description', 'profile_image')
    search_fields = ('email', 'first_name', 'last_name', 'nick_name', 'phone_number', 'nationality', 'country', 'city', 'postal_code')
    list_filter = ('nationality', 'country', 'city')
    ordering = ('-created_date',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'nick_name', 'phone_number', 'nationality', 'country', 'city', 'postal_code', 'description', 'profile_image')
        }),
        ('Important dates', {
            'fields': ('created_date',)
        }),
    )
    readonly_fields = ('created_date',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_date', 'viewer_count')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_filter = ('created_date',)

    def author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    author_name.short_description = 'Author Name'

