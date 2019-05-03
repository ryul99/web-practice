from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_time = models.DateTimeField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    date_time = models.DateTimeField()
    user = models.ForeignKey('User', on_delete = models.CASCADE)
    post = models.ForeignKey('Post', on_delete = models.CASCADE)