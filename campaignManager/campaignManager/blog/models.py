from django.db import models
from django.contrib.auth.models import User
from campaignManager.settings import UPLOAD_PATH
import datetime

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(User)
    teaser = models.TextField()
    content = models.TextField(blank=True, null=True)
    header = models.ImageField(blank=True, null=True, upload_to=UPLOAD_PATH)
    live_date = models.DateField(default=datetime.datetime.now())
    published = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-live_date', 'title']
    
    def __unicode__(self):
        return self.title