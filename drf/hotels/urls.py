import oauth2_provider.views as oauth2_views
from django.urls import include, re_path
from rest_framework import routers

from hotels.views import api as views_api

app_name = 'hotels'

router = routers.DefaultRouter()
router.register(r'hotels', views_api.HotelViewSet)
router.register(r'rooms', views_api.RoomViewSet)
router.register(r'rates', views_api.RateViewSet)
router.register(r'inventories', views_api.InventoryViewSet)

oauth2_endpoint_views = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'^access_token/$', oauth2_views.TokenView.as_view(), name="access_token"),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^oauth2/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),
    re_path(r'availability/(?P<hotel_code>.+)/(?P<checkin_date>.+)/(?P<checkout_date>.+)/$', views_api.availability, name='availability'),
    ]
