from rgb_cie import Converter
import qhue
import requests
import math


username = 'ejLH4WtpkUuagMV4epRQRxA04uyBnQaesVnxAMxF'
ip = '192.168.0.100'
change_treshold = 0.05

def get_lamp_id_by_name(bridge, lampname):
    lights = bridge.lights()
    for lightid,light in lights.items():
        if light['name'] == lampname:
            return lightid
    
    return None

class Lamp():
    
    converter = Converter()
    
    def __init__(self, lampname):
        self.name = lampname
        self.bridge = qhue.Bridge(ip, username)
        self.lampid = get_lamp_id_by_name(self.bridge, lampname)
        self.url = self.bridge.lights[self.lampid].url + '/state'
        self.on = self.bridge.lights[self.lampid]()['state']['on']
        self.xy = self.bridge.lights[self.lampid]()['state']['xy']
        self.brightnessPercent = self.bridge.lights[self.lampid]()['state']['bri'] / 255.0

    def set_color_rgb(self, r, g, b, brightnessPercent = None):
        xy = self.converter.rgbToCIE1931(r, g, b)
        self.set_color_xy(xy, brightnessPercent)
        
        
    def set_color_xy(self, xyval, brightnessPercent = None):
        xdiff = math.fabs(xyval[0] - self.xy[0])
        ydiff = math.fabs(xyval[1] - self.xy[1])
        color_diffpercent = (xdiff + ydiff) / 1.0
        
        if brightnessPercent is None:
            brightnessPercent = self.brightnessPercent        
        brightness_diffpercent = math.fabs(self.brightnessPercent - brightnessPercent)
        
        if color_diffpercent < change_treshold and brightness_diffpercent < change_treshold:
            return
        
        
        if brightnessPercent < 0.05:
            requests.put(self.url, data='{ "on": false, "transitiontime" : 0}')
            self.on = False
        else:
            if self.on == True:
                requests.put(url=self.url, data='{ "xy": [' + str(xyval[0]) + ', ' + str(xyval[1]) + '], "bri": ' + str(int(brightnessPercent * 255)) + ', "transitiontime": 1}')
            else:
                requests.put(self.url, data='{ "xy": [' + str(xyval[0]) + ', ' + str(xyval[1]) + '], "bri": ' + str(int(brightnessPercent * 255)) + ', "on": true, "transitiontime": 1}')
                self.on = True
        
        self.xy = xyval
        