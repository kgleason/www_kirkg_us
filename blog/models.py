from email.mime import image
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdownx.models import MarkdownxField
import datetime

STATUS = (
    (0,'Draft'),
    (1,'Published')
)
# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateField(null=True)
    status = models.IntegerField(choices=STATUS)
    md_content = MarkdownxField(null=True, blank=True)
    summary_text = models.CharField(max_length=500)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.publish_date <= now

class Media(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    file = models.FileField(upload_to='files/')
    image = models.ImageField(upload_to='images/')
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Media file'
        verbose_name_plural = 'Media'