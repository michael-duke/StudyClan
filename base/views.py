from django.shortcuts import render
from .models import Room
# Create your views here.

# rooms = [
#   { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
#   { 'id': 2, 'name': 'Let\'s learn React' },
#   { 'id': 3, 'name': 'React Native Developers Assemble' },
# ]

def home(request):
    rooms = Room.objects.all().order_by('id')
    context = { 'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, roomid):
    try:
        room = Room.objects.get(id=roomid)
    except Room.DoesNotExist:
        room = None
        
    context = { 'room': room}
    errormsg = { 'error': 'Room not found', 'room': room }
    if room is None:
        return render(request, 'base/room.html', errormsg)
    else:
        return render(request, 'base/room.html', context)
