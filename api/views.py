from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from base.models import Room

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/v1/',
        'GET /api/v1/rooms/',
        'GET /api/v1/rooms/<int:roomid>/',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, roomid):
    room = Room.objects.get(id=roomid)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)