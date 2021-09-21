import json
from datetime import datetime

from django.db.models import Case, Q, Sum, When
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from hotels.models import *
from hotels.serializers import *
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.none()
    serializer_class = HotelSerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'code'

    def get_queryset(self):
        queryset = Hotel.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('code', u''):
                    queryset = queryset.filter(code=self.request.GET['code'])
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
            except:
                queryset = []
        return queryset

    @method_decorator(cache_page(60*30))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @method_decorator(cache_page(60*30))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.none()
    serializer_class = RoomSerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'code'

    def get_queryset(self):
        queryset = Room.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('code', u''):
                    queryset = queryset.filter(code=self.request.GET['code'])
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
            except:
                queryset = []
        return queryset

    @method_decorator(cache_page(60*60*4))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @method_decorator(cache_page(60*60*4))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.none()
    serializer_class = RateSerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'code'

    def get_queryset(self):
        queryset = Rate.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('code', u''):
                    queryset = queryset.filter(code=self.request.GET['code'])
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
            except:
                queryset = []
        return queryset
    
    @method_decorator(cache_page(60*5))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @method_decorator(cache_page(60*5))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.none()
    serializer_class = InventorySerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Inventory.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
            except:
                queryset = []
        return queryset


@api_view(['GET'])
@authentication_classes((BasicAuthentication, OAuth2Authentication,))
@permission_classes((IsAuthenticated,))
def availability(request, hotel_code, checkin_date, checkout_date):
    """
    Returns information about free rooms for a hotel in the dates indicated
    """
    response = {}
    date_format = '%Y-%m-%d'

    try:
        checkin_date = datetime.strptime(checkin_date, date_format)
    except:
        response['error'] = 'checkin_date format must be yyyy-mm-dd'
        return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)

    try:
        checkout_date = datetime.strptime(checkout_date, date_format)
    except:
        response['error'] = 'checkout_date format must be yyyy-mm-dd'
        return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)
    
    if checkin_date < checkout_date:
        days = (checkout_date - checkin_date).days
    else:
        response['error'] = 'checkout_date must be grater than checkin_date'
        return HttpResponse(json.dumps(response), status=status.HTTP_400_BAD_REQUEST)

    # We need to check if we have a free rooms all the days between the dates
    rates = Rate.objects.prefetch_related('room__hotel').prefetch_related('inventory_set').filter(room__hotel__code=hotel_code).filter(inventory__date__gte=checkin_date, inventory__date__lt=checkout_date, inventory__quota__gt=0).annotate(free_days=Sum(Case(When(inventory__quota__gt=0, then=1)))).filter(free_days=days)

    room_codes = rates.values_list('room__code', flat=True)
    response['rooms'] = []
    for room_code in room_codes:
        room_dict = {room_code: {'rates': []}}

        for rate in rates.filter(room__code=room_code):
            rate_dict = {rate.code: {"breakdown": {}}}
            total_price = 0

            for inventory in rate.inventory_set.filter(date__gte=checkin_date, date__lt=checkout_date):
                rate_dict[rate.code]["breakdown"][str(inventory.date)] = {'price': inventory.price.to_eng_string(), 'quota': inventory.quota}
                total_price += inventory.price
            rate_dict[rate.code]['total_price'] = total_price.to_eng_string()

            room_dict[room_code]['rates'].append(rate_dict.copy())
        response['rooms'].append(room_dict)

    return HttpResponse(json.dumps(response), status=status.HTTP_200_OK)
