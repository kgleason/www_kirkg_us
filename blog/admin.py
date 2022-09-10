from django.contrib import admin
from .models import Post, Media

class MediaInlineAdmin(admin.StackedInline):
    model = Media

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'publish_date', )
    list_filter = ('status', )
    search_fields = ('title', 'md_content', )

    inlines = [MediaInlineAdmin,]

    actions = ['status_draft', 'status_publish', ]

    @admin.action(description="Draft")
    def status_draft(self, request, queryset):
        updated = queryset.update(status=0)
        self.message_user(request, f"{updated} posts we set to draft")

    @admin.action(description="Publish")
    def status_publish(self, request, queryset):
        updated = queryset.update(status=1)
        self.message_user(request, f"{updated} posts we set to draft")


class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'file', 'posts')
    list_filter = ('posts', )
    search_fields = ('title', 'image', 'file')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)