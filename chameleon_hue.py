from PIL import ImageGrab
from hue_controls import Lamp
from PIL.ImageEnhance import Brightness
import time

class HueChameleon:
    
    
    def __init__(self, lampname):
        self.lamp = Lamp(lampname)
        
        
    def tick(self):
        #taking screenshot
        screenshot_before = time.time()
        screenshot = ImageGrab.grab()
        screenshot_after = time.time()
        print '\tTaking screenshot took {} ms'.format((screenshot_after - screenshot_before) * 1000.0)

        # Getting avg color of screen
        R = 0
        G = 0
        B = 0
        
        for countAndPixel in screenshot.getcolors(1000000):
            count = countAndPixel[0]
            pixel = countAndPixel[1]
            R += pixel[0] * count
            G += pixel[1] * count
            B += pixel[2] * count

        R /= (screenshot.width * screenshot.height)
        G /= (screenshot.width * screenshot.height)
        B /= (screenshot.width * screenshot.height)
        BrightnessPercentage = (R + G + B) / (255.0*3)
        
#       print R, G, B, BrightnessPercentage    
        self.lamp.set_color_rgb(R, G, B, BrightnessPercentage)
        