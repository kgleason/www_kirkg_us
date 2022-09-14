from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).exclude(publish_date__isnull=True).order_by('-publish_date')
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class AboutMe(generic.TemplateView):
    template_name = 'about_me.html'