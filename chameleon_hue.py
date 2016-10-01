from PIL import ImageGrab
from hue_controls import Lamp
import time
from queue import Queue
from threading import Thread

class HueChameleon:
    
    
    def __init__(self, lampname):
        self.lamp = Lamp(lampname)
        self.lampStateQueue = Queue(1)
        self.lampChangerThread = Thread(target = self.lampStateChange)
        self.lampChangerThread.start()
        
    def lampStateChange(self):        
        while True:
            state = self.lampStateQueue.get()
            #lamp_before = time.time()
            self.lamp.set_color_rgb(state[0], state[1], state[2], state[3])
            #lamp_after = time.time()
            #print('\tChanging lamp state took {} ms'.format((lamp_after - lamp_before) * 1000.0))

        
    def tick(self):
        global lampChangerThread
        #taking screenshot
        #screenshot_before = time.time()
        screenshot = ImageGrab.grab()
        #screenshot_after = time.time()
        #print('\tTaking screenshot took {} ms'.format((screenshot_after - screenshot_before) * 1000.0))

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
        
        # Wait for lampthread to finish
        #wait_before = time.time()
        self.lampStateQueue.put((R,G,B,BrightnessPercentage))
        #wait_after = time.time()
        #print('\tHad to wait for lampthread for {} ms'.format((wait_after - wait_before) * 1000.0))
        
        
        
        