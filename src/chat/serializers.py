from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Message
        fields = ['author', 'content', 'created_at']