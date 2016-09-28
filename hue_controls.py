from rgb_cie import Converter
import qhue
from tornado.httpclient import HTTPClient, HTTPRequest
import tornado.web
import requests


username = 'ejLH4WtpkUuagMV4epRQRxA04uyBnQaesVnxAMxF'
ip = '192.168.0.100'

def get_lamp_id_by_name(bridge, lampname):
    lights = bridge.lights()
    for lightid,light in lights.items():
        if light['name'] == lampname:
            return lightid
    
    return None


def handleResponse(self, response):
        print("callback")
        print(response.body)

class Lamp(tornado.web.RequestHandler):
    
    converter = Converter()
    
    def __init__(self, lampname):
        self.name = lampname
        self.bridge = qhue.Bridge(ip, username)
        self.lampid = get_lamp_id_by_name(self.bridge, lampname)
        self.url = self.bridge.lights[self.lampid].url + '/state'
        self.http_client = HTTPClient()
        self.on = 


    def set_color_rgb(self, r, g, b, brightnessPercent = None):
        xy = self.converter.rgbToCIE1931(r, g, b)
        self.set_color_xy(xy, brightnessPercent)
        
        
    @tornado.web.asynchronous
    def set_color_xy(self, xyval, brightnessPercent = None):
        if brightnessPercent == None:
            self.on = True
            requests.put(self.url, data='{ "xy": [' + xyval[0] + ', ' + xyval[1] + '], "on": true, "transitiontime" = 0}')
            #self.bridge.lights[self.lampid].state(xy = xyval, on = True, transitiontime = 0)
        elif brightnessPercent < 0.05:
            requests.put(self.url, data='{ "on": false, "transitiontime" = 0}')
            #self.bridge.lights[self.lampid].state(on = False, transitiontime = 0)
        else:
            self.http_client.fetch(HTTPRequest(url=self.url, method="PUT", body='{ "xy": [' + str(xyval[0]) + ', ' + str(xyval[1]) + '], "bri": ' + str(int(brightnessPercent * 255)) + ', "on": true, "transitiontime": 0}'))
            #requests.put(self.url, data='{ "xy": [' + str(xyval[0]) + ', ' + str(xyval[1]) + '], "bri": ' + str(int(brightnessPercent * 255)) + ', "on": true, "transitiontime": 0}')
            #self.bridge.lights[self.lampid].state(xy = xyval, bri = int(brightnessPercent * 255), on = True, transitiontime = 0)
        
        tornado.ioloop.IOLoop.instance().start()