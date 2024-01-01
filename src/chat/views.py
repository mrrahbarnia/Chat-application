import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import ChatRoom

@login_required(login_url='chat:login')
def index(request):
    user = request.user
    chat_rooms = ChatRoom.objects.filter(members=user)
    context = {

        'chat_rooms': chat_rooms

    }
    return render(request, 'chat/index.html', context)

@login_required(login_url='chat:login')
def room(request, room_name):

    user = request.user
    username = request.user.username

    context = {
        'room_name': room_name,
        'username': mark_safe(json.dumps(username))
    }

    chat_room = ChatRoom.objects.filter(name=room_name).first()
    if chat_room:
        chat_room.members.add(user)
    else:
        chat_room = ChatRoom.objects.create(name=room_name)
        chat_room.members.add(user)
    # context.update({'chat_room': room_name})

    return render(request, 'chat/room.html', context)