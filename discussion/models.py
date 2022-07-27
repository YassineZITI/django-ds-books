from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Category
from django.urls import reverse



class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='topic')

    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='userpost')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,related_name='topicpost')
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        
        return reverse('posts')
   


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='usercomment')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='postcomment')
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.post})