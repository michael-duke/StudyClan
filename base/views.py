from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse("Hello World")

def room(request):
    return HttpResponse("You're looking at room")