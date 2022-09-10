from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from .models import Post, Media

class MediaInlineAdmin(admin.StackedInline):
    model = Media

class PostUpdateActionForm(ActionForm):
    status = forms.ModelChoiceField(Post.STATUS, required=False)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'publish_date', )
    list_filter = ('status', )
    search_fields = ('title', 'md_content', )

    inlines = [MediaInlineAdmin,]

    actions = ['post_status']

    action_form = PostUpdateActionForm

    @admin.action(description="UpdateStatus")
    def post_status(self, request, queryset):
        updated = queryset.update(status=request.POST['status'])
        self.message_user(request, f"{updated} posts we set to {request.POST['status']}")

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'file', 'posts')
    list_filter = ('posts', )
    search_fields = ('title', 'image', 'file')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Media, MediaAdmin)