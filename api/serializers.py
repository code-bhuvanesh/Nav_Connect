from .models import Driver,Bus, Routes,SubRoutes,Location,User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)  # Make email optional

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'user_type']
    
    def create(self, validated_data):
        # Create User instance with password hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        return user
    
class DriverSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', required=False)  # Email is not required
    user = UserSerializer()  # Nested serializer

    class Meta:
        model = Driver
        fields = ['id', 'name', 'phone_number', 'email', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        driver = Driver.objects.create(user=user, **validated_data)
        return driver
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()

        # Update the Driver instance
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        return instance


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
# 