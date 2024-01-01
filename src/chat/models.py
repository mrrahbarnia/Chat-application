from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ChatRoom(TimeStamp):
    name = models.CharField(max_length=250)
    members = models.ManyToManyField(user, related_name='chat_room_members')

    def __str__(self):
        return self.name


class Message(TimeStamp):
    author = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name='message_author'
    )
    content = models.TextField()
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='message_chat_room'
    )

    def last_messages(self, room_name):
        qs = Message.objects.filter(chat_room__name=room_name).order_by('-created_at').all()
        return qs

    def __str__(self):
        return f"'{self.content[:20]}' FROM '{self.author.username}'"
