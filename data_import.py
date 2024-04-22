import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "navconnect.settings")

django.setup()
from django.contrib.auth.models import User
from api.models import DriverView, User
import csv

def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    return user

def create_driver(user, name, phone_number):
    driver = DriverView.objects.create(user=user, name=name, phone_number=phone_number)
    return driver

def insert_data_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create user
            username = row['name']  
            password = row['password']  
            user = create_user(username, password)
            
            # Create driver
            name = row['name']
            phone_number = row['phone_number']
            create_driver(user, name, phone_number)

if __name__ == "__main__":
    csv_file_path = "bus_csv.csv"
    insert_data_from_csv(csv_file_path)
