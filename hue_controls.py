from rgb_cie import Converter
import qhue

username = 'ejLH4WtpkUuagMV4epRQRxA04uyBnQaesVnxAMxF'
ip = '192.168.0.100'

def get_lamp_id_by_name(bridge, lampname):
    lights = bridge.lights()
    for lightid,light in lights.iteritems():
        if light['name'] == lampname:
            return lightid
    
    return None


class Lamp:
    
    converter = Converter()
    
    def __init__(self, lampname):
        self.name = lampname
        self.bridge = qhue.Bridge(ip, username)
        self.lampid = get_lamp_id_by_name(self.bridge, lampname)


    def set_color_rgb(self, r, g, b, brightnessPercent = None):
        xy = self.converter.rgbToCIE1931(r, g, b)
        self.set_color_xy(xy, brightnessPercent)
        
    def set_color_xy(self, xyval, brightnessPercent = None):
        if brightnessPercent == None:
            self.bridge.lights[self.lampid].state(xy = xyval, on = True, transitiontime = 0)
        elif brightnessPercent < 0.05:
            self.bridge.lights[self.lampid].state(on = False, transitiontime = 0)
        else:
            self.bridge.lights[self.lampid].state(xy = xyval, bri = int(brightnessPercent * 255), on = True, transitiontime = 0)
            