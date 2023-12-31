from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Message(TimeStamp):
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='message_author'
    )
    content = models.TextField()

    def last_messages():
        qs = Message.objects.order_by('-created_at').all()
        return qs

    def __str__(self):
        return f"'{self.content[:20]}' FROM '{self.author.username}'"
