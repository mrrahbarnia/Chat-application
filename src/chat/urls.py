from django.urls import path
from django.contrib.auth.views import LoginView

from .views import index, room

app_name = 'chat'

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
    path('login', LoginView.as_view(template_name='chat/login.html'), name='login')
]