from django.shortcuts import render

# Create your views here.

rooms = [
  { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
  { 'id': 2, 'name': 'Let\'s learn React' },
  { 'id': 3, 'name': 'React Native Developers Assemble' },
]
def home(request):
    context = { 'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, roomid):
    room = None
    for r in rooms:
        if r['id'] == roomid:
            room = r
            break
    context = { 'room': room}
    errormsg = { 'error': 'Room not found', 'room': room }
    if room is None:
        return render(request, 'base/room.html', errormsg)
    else:
        return render(request, 'base/room.html', context)
