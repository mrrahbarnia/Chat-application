import json

from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

from .models import Message, ChatRoom
from .serializers import MessageSerializer

user = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def new_message(self, dict_data):
        room_name = dict_data['chat_room']
        chat_model = ChatRoom.objects.get(name=room_name)
        author = dict_data['username']
        message = dict_data['message']
        user_instance = user.objects.get(username=author)
        message_model = Message.objects.create(
            author=user_instance, content=message
            , chat_room=chat_model
        )


        result = eval(self.message_serializer(message_model))
        self.send_message(result)


    def fetch_message(self, data):
        room_name = data['chat_room']
        qs = Message.last_messages(self, room_name=room_name)
        message = self.message_serializer(qs)
        content = {
            'command': 'fetch_message',
            'message': eval(message)
            }
        self.chat_message(content)
        pass


    def message_serializer(self, qs):
        many = (lambda qs: True if (qs.__class__.__name__=='QuerySet') else False)(qs)
        serialized = MessageSerializer(qs, many=many)
        message = JSONRenderer().render(serialized.data)
        return message


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()


    commands = {
        'new_message': new_message,
        'fetch_message': fetch_message
    }


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        command = text_data_dict["command"]

        self.commands[command](self, text_data_dict)


    def send_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'command': 'new_message',
                'author': message['author'],
                'content': message['content'],
            }
        )


    def chat_message(self, event):
        async_to_sync(self.send(text_data=json.dumps(event)))
