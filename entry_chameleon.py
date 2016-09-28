import sys
from chameleon_hue import HueChameleon
import time


if __name__ == '__main__':
    lamp_name = sys.argv[1]

    last_tick = time.time()
    chameleon = HueChameleon(lamp_name)
    while True:
        chameleon.tick()
        current_time = time.time()
        ms_spent = (current_time - last_tick) * 1000.0
        print('This tick took {} ms. Tick rate = {}'.format(ms_spent, 1000.0 / ms_spent))
        last_tick = current_time
        #time.sleep(1/15.0)
