from django.urls import path
from .views import CreateBus, BusDetails, CreateRoute, DriverView, TestEsp32
from .views import CreateBus, BusDetails, CreateRoute, DriverView, SearchRoute

urlpatterns = [
    path('drivers/', DriverView.as_view(), name='driver-detail'),
    # path('drivers/create/', CreateDriver.as_view(), name='create-driver'),
    # path('drivers/update/<int:pk>/', UpdateDriver.as_view(), name='update-driver'),
    # path('drivers/delete/<int:pk>/', DeleteDriver.as_view(), name='delete-driver'),
    path('createbus/', CreateBus.as_view(), name='create_bus_api'),
    path('createroute/', CreateRoute.as_view(), name='create_route_api'),
    path('busdetails/', BusDetails.as_view(), name='bus_create_api'),
    path("esp32/", TestEsp32.as_view(), name="test esp32")
]
