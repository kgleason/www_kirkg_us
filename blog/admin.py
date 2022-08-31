from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post


class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'slug', 'status', 'publish_date', )
    list_filter = ('status', )
    search_fields = ('title', 'md_content', )


# Register your models here.
admin.site.register(Post, PostAdmin)