from django.shortcuts import render

# Create your views here.

rooms = [
  { 'id': 1, 'name': 'Let\'s learn Django RESTful API' },
  { 'id': 2, 'name': 'Let\'s learn React' },
  { 'id': 3, 'name': 'React Native Developers Assemble' },
]
def home(request):
    context = { 'rooms': rooms}
    return render(request, 'home.html', context)

def room(request):
    return render(request, 'room.html')