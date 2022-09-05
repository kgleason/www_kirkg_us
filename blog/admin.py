from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Media

class MediaInlineAdmin(admin.StackedInline):
    model = Media

class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'slug', 'status', 'publish_date', )
    list_filter = ('status', )
    search_fields = ('title', 'md_content', )

    inlines = [MediaInlineAdmin,]

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'file', 'posts')
    list_filter = ('posts', )
    search_fields = ('title', 'image', 'file')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)