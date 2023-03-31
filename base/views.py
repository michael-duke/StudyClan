from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

# rooms = [
#   { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
#   { 'id': 2, 'name': 'Let\'s learn React' },
#   { 'id': 3, 'name': 'React Native Developers Assemble' },
# ]

def home(request):
    rooms = Room.objects.all()
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
    
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    form = RoomForm(instance=room)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    context = {'item': room}
    return render(request, 'base/delete.html', context)