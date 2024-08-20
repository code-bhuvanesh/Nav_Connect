import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DriverSerializer, BusSerializer, RoutesSerializer, SubRoutesSerializer
from .models import Driver, Bus, LocationGeo, Routes, Location, SubRoutes, User
from routestTest import getBusDetails 
from django.db.models import Q
import requests as httpreq
from django.shortcuts import get_object_or_404



class DriverView(APIView):
    def get(self, request):
        drivers = Driver.objects.all()
        serializer_all = DriverSerializer(drivers, many=True)
        pk = request.data.get("pk")
        if pk:
            driver = Driver.objects.get(id=pk)
            serializer_specific = DriverSerializer(driver)
            return Response({
                'all_drivers': serializer_all.data,
                'specific_driver': serializer_specific.data
            })
        else:
            return Response(serializer_all.data)
        
    def post(self, request):
        driver_serializer = DriverSerializer(data=request.data)
        if driver_serializer.is_valid():
            driver_serializer.save()
            return Response(driver_serializer.data, status=status.HTTP_201_CREATED)
        return Response(driver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        driver = Driver.objects.get(id=pk)
        serializer = DriverSerializer(instance=driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        driver = Driver.objects.get(id=pk)
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CreateBus(APIView):
    def get_object(self, pk):
        return get_object_or_404(Bus, pk=pk)
    
    def post(self, request):
        serializer = BusSerializer(data=request.data)
        
        if serializer.is_valid():
            bus = serializer.save()
            bus.location = Location.objects.create()
            bus.save()
            return Response({"response" : "ok" }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        bus = self.get_object(pk)
        if bus is None:
            return Response({"error": "Bus not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BusSerializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response" : "ok" }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        bus = self.get_object(pk)
        bus.delete()
        return Response({"message": "Bus deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
        
class BusDetails(APIView):
    def get(self, request):
        buses = Bus.objects.all() #add query that driver and route is not null
        bus_data = []
        for bus in buses:
            driver_name = bus.driver.name
            if(bus.location != None):
                bus_lat = bus.location.current_latitude 
                bus_lang = bus.location.current_longitude 
            else:
                bus_lat = 0.0 
                bus_lang = 0.0

            route_id = bus.route
            route_data = []
            routes = SubRoutes.objects.filter(route=route_id.id)
            print(routes)
            for route in routes:
                route_data.append( {
                    "route_name": route.route_name,
                    "order": route.order,
                    "lat": route.location.current_latitude,
                    "lang": route.location.current_longitude
                })
            
            bus_details = {
                "route_id": route_id.id,
                "bus_id": bus.id,
                "bus_no": bus.busno,
                "driver_id": bus.driver.id,
                "driver_name": driver_name,
                "bus_lat": bus_lat,
                "bus_lang": bus_lang,
                "route_title" : route_id.route_title,
                "routes": route_data
            }
            bus_data.append(bus_details)
        
        return Response(bus_data)
    
    
class CreateRoute(APIView):
    def post(self, request):
        route_data = request.data.get('route_title', "")
        subroutes_data = request.data.get('subroutes', [])
        print(route_data)
        print(subroutes_data[0])
        # Validate route data
        route_serializer = RoutesSerializer(data=request.data)
        if not route_serializer.is_valid():
            print("route title not created")
            return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        route_instance = route_serializer.save()

        # Validate and save subroutes
        for subroute_data in subroutes_data:
            subroute_data['route'] = route_instance.id  # Associate subroute with the route
            print(subroute_data)
            loc = subroute_data["location"]
            loc_instance = Location.objects.create(current_latitude=loc["lat"], current_longitude=loc["lang"])
            subroute_data["location"] = loc_instance.id
            subroute_serializer = SubRoutesSerializer(data=subroute_data)
            if subroute_serializer.is_valid():
                subroute_serializer.save()
            else:
                print("sub route not created")
                route_instance.delete()
                return Response(subroute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"response" : "ok" }, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        routes = Routes.objects.all()
        data = []

        for route in routes:
            route_data = RoutesSerializer(route).data
            route_data['route_id'] = route.id
            subroutes_data = SubRoutesSerializer(route.subroutes_set.all(), many=True).data
            route_data['subroutes'] = subroutes_data
            data.append(route_data)

        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        route = get_object_or_404(Routes, pk=pk)
        Bus.objects.filter(route=route).update(route=None)
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        route_instance = get_object_or_404(Routes, pk=pk)
        route_serializer = RoutesSerializer(route_instance, data=request.data, partial=True)

        if route_serializer.is_valid():
            # Save the updated route instance
            route_instance = route_serializer.save()
            
            # Get the subroutes data from the request
            subroutes_data = request.data.get('subroutes', [])
            existing_subroutes_ids = set(route_instance.subroutes_set.values_list('id', flat=True))
            updated_subroutes_ids = set()

            for subroute_data in subroutes_data:
                subroute_id = subroute_data.get('id')
                if subroute_id:
                    # Update existing subroute
                    subroute_instance = get_object_or_404(SubRoutes, id=subroute_id)
                    subroute_serializer = SubRoutesSerializer(subroute_instance, data=subroute_data, partial=True)
                    if subroute_serializer.is_valid():
                        subroute_serializer.save()
                        updated_subroutes_ids.add(subroute_id)
                    else:
                        return Response(subroute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Create new subroute
                    subroute_data['route'] = route_instance.id
                    loc_data = subroute_data.get('location', {})
                    loc_instance = Location.objects.create(
                        current_latitude=loc_data.get('lat'),
                        current_longitude=loc_data.get('lang')
                    )
                    subroute_data['location'] = loc_instance.id
                    subroute_serializer = SubRoutesSerializer(data=subroute_data)
                    if subroute_serializer.is_valid():
                        subroute_serializer.save()
                    else:
                        return Response(subroute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Delete subroutes that are no longer in the request
            subroutes_to_delete = existing_subroutes_ids - updated_subroutes_ids
            SubRoutes.objects.filter(id__in=subroutes_to_delete).delete()

            return Response(route_serializer.data, status=status.HTTP_200_OK)

        return Response(route_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class TestEsp32(APIView):
    def get(self, request):
        print("get method")
        print(request.query_params )
        print(request.data)
        return Response("response ok", status=status.HTTP_200_OK)
    def post(self, request):
        print("post method")
        print(request.data)
        return Response("response ok", status=status.HTTP_200_OK)
    
    def get(self, request):
        routes = Routes.objects.all()
        data = []

        for route in routes:
            route_data = RoutesSerializer(route).data
            route_data['route_id'] = route.id
            subroutes_data = SubRoutesSerializer(route.subroutes_set.all(), many=True).data
            route_data['subroutes'] = subroutes_data
            data.append(route_data)

        return Response(data, status=status.HTTP_200_OK)

   
class SearchRoute(APIView):
    def get(self, requests):
        name = requests.query_params.get("route")
        allroutes = {}
        if( name == None and name == ''):
            allroutes = LocationGeo.objects.all()
        else:
            allroutes = LocationGeo.objects.filter(Q(routeName__startswith=name[:1]) & Q(routeName__contains=name)).values()
        return Response(allroutes)
    
    def post(self, request):
        name = request.data.get("route")
        apikey = "5b3ce3597851110001cf6248e39436fe480248a0901675a1fe89ff0e"
        url = f'https://api.openrouteservice.org/geocode/search?api_key={apikey}&text={name}&focus.point.lon=80.007935&focus.point.lat=13.020614&boundary.country=IN&sources=openstreetmap,openaddresses&layers=street,venue&size=1'
        result = httpreq.get(url)
        print(json.loads(result.content))
        print(name)
        data = json.loads(result.content)["features"]
        if(data != None and len(data) != 0):
            data = data[0]["geometry"]["coordinates"]
            print(data)
            if not LocationGeo.objects.filter(routeName=name).exists():
                loc = Location.objects.create(current_latitude=data[1], current_longitude=data[0])
                LocationGeo.objects.create(routeName = name, location = loc)
            return Response({
                "lang" : data[0],
                "lat" : data[1]
            }, status=status.HTTP_200_OK)
        return Response({"status" : False,
                         "response" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)

test_route = {
    "route" : "porur",
    "subroutes" : [
        {
            "route_name" : "Velachery",
            "lat" : 23.2,
            "lang" : 21.2
        },
        {
            "route_name" : "Velachery",
            "lat" : 23.2,
            "lang" : 21.2
        },
        {
            "route_name" : "Velachery",
            "lat" : 23.2,
            "lang" : 21.2
        },
    ]
}



# class BusCreation(APIView):
#     def post(self, request):
#         serializer = BusCreationSerializer(data=request.data)
#         if serializer.is_valid():
#             bus_no = serializer.validated_data['bus_no']
#             driver = Driver.objects.all()[0]
#             bus = Bus.objects.create(busno=bus_no, driver=driver)
            # routes_data = serializer.validated_data['routes']
            # print(Driver.objects.all())
            # location_bus = Location.objects.create(current_latitude=0, current_longitude=0)
            # for route_data in routes_data:
            #     routename = route_data['route_name']
            #     order = route_data['order']
            #     lat = route_data['lat']
            #     lang = route_data['lang']
            #     location = Location.objects.create(current_latitude=lat, current_longitude=lang)
            #     route = SubRoutes.objects.create(route_name=routename, order=order, location=location,bus_id=bus.id)
        #     return Response("Bus and routes created successfully", status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class BusDetails(APIView):
#     def get(self, request):
#         buses = Bus.objects.all()
#         bus_data = []
#         for bus in buses:
#             driver_name = bus.driver.name 
#             bus_lat = bus.location.current_latitude 
#             bus_lang = bus.location.current_longitude 
            
#             routes_data = []
#             routes = Routes.objects.filter(bus_id=bus.id)
#             for route in routes:
#                 route_data = {
#                     "route_name": route.route_name,
#                     "order": route.order,
#                     "lat": route.location.current_latitude,
#                     "lang": route.location.current_longitude
#                 }
#                 routes_data.append(route_data)
            
#             bus_details = {
#                 "bus_id": bus.id,
#                 "bus_no": bus.busno,
#                 "driver_id": bus.driver.id,
#                 "driver_name": driver_name,
#                 "bus_lat": bus_lat,
#                 "bus_lang": bus_lang,
#                 "routes": routes_data
#             }
#             bus_data.append(bus_details)
#         newBuses = getBusDetails()
#         print("newBuses")
#         bus_data += newBuses
#         print(bus_data)
#         return Response(bus_data)

#check if the driver not allocated to any bus
# class BusCreation(APIView):
#     def post(self, request):
#         serializer = BusCreationSerializer(data=request.data)
#         if serializer.is_valid():
#             bus_no = serializer.validated_data['bus_no']
#             driver = Driver.objects.all()[0]
#             bus = Bus.objects.create(busno=bus_no, driver=driver)
            # routes_data = serializer.validated_data['routes']
            # print(Driver.objects.all())
            # location_bus = Location.objects.create(current_latitude=0, current_longitude=0)
            # for route_data in routes_data:
            #     routename = route_data['route_name']
            #     order = route_data['order']
            #     lat = route_data['lat']
            #     lang = route_data['lang']
            #     location = Location.objects.create(current_latitude=lat, current_longitude=lang)
            #     route = SubRoutes.objects.create(route_name=routename, order=order, location=location,bus_id=bus.id)
        #     return Response("Bus and routes created successfully", status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class BusDetails(APIView):
#     def get(self, request):
#         buses = Bus.objects.all()
#         bus_data = []
#         for bus in buses:
#             driver_name = bus.driver.name 
#             bus_lat = bus.location.current_latitude 
#             bus_lang = bus.location.current_longitude 
            
#             routes_data = []
#             routes = Routes.objects.filter(bus_id=bus.id)
#             for route in routes:
#                 route_data = {
#                     "route_name": route.route_name,
#                     "order": route.order,
#                     "lat": route.location.current_latitude,
#                     "lang": route.location.current_longitude
#                 }
#                 routes_data.append(route_data)
            
#             bus_details = {
#                 "bus_id": bus.id,
#                 "bus_no": bus.busno,
#                 "driver_id": bus.driver.id,
#                 "driver_name": driver_name,
#                 "bus_lat": bus_lat,
#                 "bus_lang": bus_lang,
#                 "routes": routes_data
#             }
#             bus_data.append(bus_details)
#         newBuses = getBusDetails()
#         print("newBuses")
#         bus_data += newBuses
#         print(bus_data)
#         return Response(bus_data)