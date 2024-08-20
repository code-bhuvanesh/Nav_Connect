from django.urls import path
from .views import CreateBus, BusDetails, CreateRoute, DriverView, TestEsp32
from .views import CreateBus, BusDetails, CreateRoute, DriverView, SearchRoute

urlpatterns = [
    path('drivers/', DriverView.as_view(), name='driver-detail'),
    path('drivers/<int:pk>/', DriverView.as_view(), name='update-driver'),
    path('drivers/<int:pk>/', DriverView.as_view(), name='delete-driver'),
    path('createroute/', CreateRoute.as_view(), name='create_route_api'),
    path('createroute/<int:pk>/', CreateRoute.as_view(), name='update-route'),
    path('createbus/', CreateBus.as_view(), name='create_bus_api'),
    path('createbus/<int:pk>/', CreateBus.as_view(), name='bus-detail'),
    path('busdetails/', BusDetails.as_view(), name='bus_create_api'),
    path("esp32/", TestEsp32.as_view(), name="test esp32"),
]
