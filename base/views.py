from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#   { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
#   { 'id': 2, 'name': 'Let\'s learn React' },
#   { 'id': 3, 'name': 'React Native Developers Assemble' },
# ]
def loginPage(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, username=username, password=password)    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(host__username__icontains=q))
    room_count = rooms.count()
    print(rooms)
    topics = Topic.objects.all()
    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count}
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
    
@login_required(login_url='login')    
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  
def updateRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  
def deleteRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    context = {'item': room}
    return render(request, 'base/delete.html', context)