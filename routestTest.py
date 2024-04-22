import random
import requests
busurl = "https://erp.sathyabama.ac.in/erp/api/v1.0/TransportRoute/routenameList"
loginurl = "https://erp.sathyabama.ac.in/erp/api/v1.0/MasterStudent/login"


def getLoginkey():
    response = requests.post(loginurl, data={"RegisterNumber": "41110198", "Password": "Bhuvideva003"})
    return response.json()["responseData"]["login"]["accessToken"]

def getBusDetails():
    loginKey = getLoginkey()
    response = requests.post(busurl, headers={"Authorization" : f"Bearer {loginKey}"}, data={"BoardingPointId": 1, "RouteDate": "", "RouteType": 1, "RouteCategory": 1})
    busdata = []
    for bus in response.json()["responseData"]:
        busno = 78
        if bus["RouteNo"].find("(") != -1:
            bus["RouteNo"] = str(bus["RouteNo"]).replace("(Contract)", "")
            busno = int(bus["RouteNo"][bus["RouteNo"].index("(") + 1 : bus["RouteNo"].index(")")])
        RouteName =  bus["RouteName"]
        if bus["RouteName"].find("-") != -1:
            RouteName =  bus["RouteName"][:bus["RouteName"].index("-")]
        RouteName = RouteName.capitalize()
        busdata.append(
            {
                "bus_id": 0,
                "bus_no": busno,
                "driver_id": 0,
                "driver_name": "",
                "bus_lat": 0.0,
                "bus_lang": 0.0,
                "routes": [{
                    "route_name": RouteName,
                    "order": 0,
                    "lat": 0.0,
                    "lang": 0.0,
                }]
            }
        )
    random.shuffle(busdata)
    return busdata 
# print(getBusDetails())