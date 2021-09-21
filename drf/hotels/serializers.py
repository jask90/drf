from hotels.models import *
from rest_framework import serializers


class HotelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Hotel
        fields = ('code', 'name')
        lookup_field = 'code'


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    hotel = serializers.SlugRelatedField(queryset=Hotel.objects.all(), slug_field='code')

    class Meta:
        model = Room
        fields = ('code', 'name', 'hotel',)
        lookup_field = 'code'


class RateSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.SlugRelatedField(queryset=Room.objects.all(), slug_field='code')

    class Meta:
        model = Rate
        fields = ('code', 'name', 'room',)
        lookup_field = 'code'


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    rate = serializers.SlugRelatedField(queryset=Rate.objects.all(), slug_field='code')

    class Meta:
        model = Inventory
        fields = ('id', 'name', 'rate', 'date', 'price', 'quota')
