from .models import Driver,Bus, Routes,SubRoutes,Location,User
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['password','first_name','last_name','email','username','user_type']
#     def create(self, validated_data):
#         # Create User instances
#         user = User.objects.create_user(**validated_data)
#         return user

class DriverSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True) 
    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone_number', 'email'] 

    def create(self, validated_data):
        driver = Driver.objects.create(**validated_data)
        return driver


# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'

# class RouteDetailSerializer(serializers.Serializer):
#     route_name = serializers.CharField()
#     order = serializers.IntegerField()
#     lat = serializers.DecimalField(max_digits=9, decimal_places=6)
#     lang = serializers.DecimalField(max_digits=9, decimal_places=6)

# class BusCreationSerializer(serializers.Serializer):
#     bus_no = serializers.IntegerField()
#     driver_id = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
        
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['busno', 'driver', 'route']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'current_latitude', 'current_longitude']
        read_only_fields = ['id'] 

class SubRoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRoutes
        fields = ['id', 'route', 'route_name', 'order', 'location']
        read_only_fields = ['id']


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ['route_title'] 


test_route = {
    "route_title" : "porur",
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