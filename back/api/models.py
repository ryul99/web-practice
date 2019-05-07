from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    update_time = models.DateTimeField(default=now)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='post_set')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'update_time': self.update_time,
            'user_id': self.user.id,
            'comment_ids': list(self.comment_set.values_list('id', flat=True).all()),
        }

class Comment(models.Model):
    content = models.TextField()
    update_time = models.DateTimeField()
    user = models.ForeignKey('User', on_delete = models.CASCADE, related_name='comment_set')
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name='comment_set')

    def as_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'update_time': self.update_time,
            'user_id': self.user.id,
        }