from email.mime import image
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
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
    md_content = MarkdownField(rendered_field='rendered_text', validator=VALIDATOR_STANDARD, null=True, blank=True)
    summary_text = MarkdownField(rendered_field='rendered_summary', validator=VALIDATOR_STANDARD, null=True, blank=True)
    rendered_text = RenderedMarkdownField(null=True)
    rendered_summary = RenderedMarkdownField(null=True)

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
    file = models.FileField(upload_to='files/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Media file'
        verbose_name_plural = 'Media'