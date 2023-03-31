from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:roomid>', views.room, name='room'),
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<int:roomid>', views.updateRoom, name='update-room'),
    path('delete-room/<int:roomid>', views.deleteRoom, name='delete-room'),
]
