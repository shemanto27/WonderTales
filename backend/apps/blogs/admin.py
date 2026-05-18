from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import BlogModel

@admin.register(BlogModel)
class BlogAdmin(ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content', 'tags')
    list_filter = ('created_at', 'updated_at')
