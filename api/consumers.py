# from channels.generic.websocket import AsyncWebsocketConsumer 

# class BusLocationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         busId = self.scope['url_route']['kwargs']["busid"]
#         print(busId)
#         await self.channel_layer.group_add("bus_loc", self.channel_name)
#         self.accept()
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("bus_loc", self.channel_name)

#     async def receive(self, data):
#         print("bus data is : ",data)
import json
from channels.generic.websocket import WebsocketConsumer 
from asgiref.sync import async_to_sync

from api.models import Bus

class BusLocationConsumer(WebsocketConsumer):

    ##todo: make login for users and create separate channels for each users to send notification about the buses separatly
    def connect(self):
        self.busId = int(self.scope['url_route']['kwargs']["busid"])
        self.group_name = f"loc_{self.busId}"
        print(self.channel_name)
        print(self.busId)
        async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name
                )

        self.accept()
        if(not Bus.objects.filter(id=self.busId).exists()):
            self.send(json.dumps(
                {"response" : "bus id is not present"}
            ))
            self.close()
        
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
            )
        

    def receive(self, text_data):
        # print(text_data)
        # self.send(text_data+"from server")
        data = json.loads(text_data)
        current_lat = data["lat"]
        current_lang = data["lang"]
        self.update_location(current_lat,current_lang)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type' : 'update_loc',
                'current_lat' : current_lat,
                'current_lang' : current_lang

            }
        )



    def update_loc(self, event):
        print("update_loc is called", event )
        current_lat = event["current_lat"]
        current_lang = event["current_lang"]
        self.send(json.dumps({
            "response" : "ok",
            'current_lat' : current_lat,
            'current_lang' : current_lang
        }))

    def update_location(self, lat,lang):
        # print(lat,lang)
        # buses = Bus.objects.filter(id=self.busId)
        # if(buses.exists()):
        #     print("bus id : ", buses[0].id)
        #     buses[0].location.current_latitude = lat
        #     buses[0].location.current_longitude = lang
        #     buses[0].location.save()
        #     print(buses[0].location.current_latitude,buses[0].location.current_longitude)
        #     buses[0].save()
        buses = Bus.objects.get(id=self.busId)
        print(buses)
        if(buses != None):
            # print(buses.location.current_latitude,buses.location.current_longitude)
            print("bus id : ", buses.id)
            buses.location.current_latitude = lat
            buses.location.current_longitude = lang
            buses.location.save()
            print(buses.location.current_latitude,buses.location.current_longitude)
            buses.save()