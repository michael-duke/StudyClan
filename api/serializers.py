from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        exclude = ['created_at', 'updated_at']