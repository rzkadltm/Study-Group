from rest_framework.serializers import ModelSerializer
from base.models import Room

# take all the room's field and turn it into json


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
