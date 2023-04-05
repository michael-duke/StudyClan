from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('room/<int:roomid>', views.room, name='room'),
    path('profile/<int:userid>', views.userProfile, name='user-profile'),
    path('create-room', views.createRoom, name='create-room'),
    path('update-room/<int:roomid>', views.updateRoom, name='update-room'),
    path('delete-room/<int:roomid>', views.deleteRoom, name='delete-room'),
    path('update-message/<int:messageid>', views.updateMessage, name='update-message'),
    path('delete-message/<int:messageid>', views.deleteMessage, name='delete-message'),
]
