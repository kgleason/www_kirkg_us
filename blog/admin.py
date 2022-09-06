from django.contrib import admin
from .models import Post, Media

class MediaInlineAdmin(admin.StackedInline):
    model = Media

class PostAdmin(admin.ModelAdmin):
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