from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview_image', 'is_published', 'views_count', 'created_at')
    list_filter = ('title', 'is_published')
    search_fields = ('title', 'created_at')
