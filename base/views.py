from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, MessageForm, UserForm, CreateUserForm
# Create your views here.

# rooms = [
#   { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
#   { 'id': 2, 'name': 'Let\'s learn React' },
#   { 'id': 3, 'name': 'React Native Developers Assemble' },
# ]
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')
        user = authenticate(request, email=email, password=password)    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, user)
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in')
        return redirect('home')
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            print(user)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occured during registration')
            return redirect('register')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(host__username__icontains=q))
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q) | Q(room__name__icontains=q) | Q(room__description__icontains=q) | Q(room__host__username__icontains=q))

    topics = Topic.objects.all()[0:5]
    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, roomid):
    try:
        room = Room.objects.get(id=roomid)
    except Room.DoesNotExist:
        room = None
    room_messages = room.message_set.all().order_by('-created_at')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            room=room,
            user=request.user,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        message.save()
        return redirect('room', roomid=room.id)
    
    context = { 'room': room, 'room_messages': room_messages, 'participants': participants}
    errormsg = { 'error': 'Room not found', 'room': room }
    if room is None:
        return render(request, 'base/room.html', errormsg)
    else:
        return render(request, 'base/room.html', context)

def userProfile(request, userid):
    user = User.objects.get(id=userid)
    # if request.user != user:
    #     return HttpResponse('You are not allowed to view this profile.')
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = { 'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)    

@login_required(login_url='login')    
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            host=request.user,
            topic=topic
        )
        return redirect('home')
        
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  
def updateRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form': form, 'room': room, 'topics': topics}
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

@login_required(login_url='login')  
def updateMessage(request, messageid):
    message = Message.objects.get(id=messageid)
    form = MessageForm(instance=message)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed to update this message')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('room', roomid=message.room.id)
        
    context = {'form': form}
    return render(request, 'base/update_message.html', context)

@login_required(login_url='login')  
def deleteMessage(request, messageid):
    message = Message.objects.get(id=messageid)
    
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
        
    context = {'item': message}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            update_user = form.save(commit=False)
            update_user.username = update_user.username.lower()
            update_user.save()
            return redirect('user-profile', userid=user.id)
    context = {'form': form}
    return render(request, 'base/update-user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/mobile.topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/mobile.activity.html', context)