import time
from  geocoder import ip
from getpass import getuser
from datetime import datetime

class UserModel():
    def __init__(self):
        self.userName = getuser()
        self.latitud = 0
        self.longitud = 0

    def getName(self):
        return self.userName

    def getLatLog(self):
        g = ip('me')
        self.latitud = g.latlng[0]
        self.longitud = g.latlng[1]
        return self.latitud, self.longitud
    
    def get_time(self):
        return time.strftime("%H:%M") 
    
    def get_date(self):
        return time.strftime("%d/%m/%Y")
    
    def fullDate(self):
        fecha_hora_actual = datetime.now()
        return fecha_hora_actual.strftime("%Y-%m-%dT%H:%M:%S")
        #return "2022:03:03T22:03:03"
