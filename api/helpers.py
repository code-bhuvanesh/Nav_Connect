from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Calculate the distance
    distance = R * c
    
    return distance

# Example usage
# lat1, lon1 = 40.7128, -74.0060  # Latitude and longitude of point 1 (New York City)
# lat2, lon2 = 34.0522, -118.2437  # Latitude and longitude of point 2 (Los Angeles)

# distance = haversine_distance(lat1, lon1, lat2, lon2)
# print(f"The distance between the two points is {distance:.2f} kilometers.")
