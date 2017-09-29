from sense_hat import SenseHat
import time

s = SenseHat()
s.set_imu_config(False, True, False)

orientation = s.get_orientation()

global left
left = False
global leftOr
leftOr = 0
global right
right = False
global rightOr
rightOr = 0
global top
top = False
global topOr
topOr = 0
global bottom
bottom = False
global bottomOr
bottomOr = 0

def check():
    if orientation['pitch'] > 315 and orientation['pitch'] < 360:
        #droite
        global right
        global rightOr
        right = True
        rightOr = 360 - orientation['pitch']
    
    if orientation['pitch'] > 0 and orientation['pitch'] < 45:
        #gauche
        global left
        global leftOr
        left = True
        leftOr = 0 + orientation['pitch']
    
    if orientation['roll'] > 315 and orientation['roll'] < 360:
        #haut
        global top
        global topOr
        top = True
        topOr = 360 - orientation['roll']

    if orientation['roll'] > 0 and orientation['roll'] < 45:
        #bas
        global bottom
        global bottomOr
        bottom = True
        bottomOr = 0 + orientation['roll']
    
    doTheMove()


def doTheMove():
    if left:
        if top:
            if leftOr > topOr:
                s.set_pixel(0, 4, 255, 0, 255)
            elif topOr > leftOr:
                s.set_pixel(4, 0, 255, 0, 255)
            else:
                s.set_pixel(4, 4, 0, 255, 255)
        elif bottom:
            if leftOr > bottomOr:
                s.set_pixel(0, 4, 255, 0, 255)
            elif bottomOr > leftOr:
                s.set_pixel(4, 7, 255, 0, 255)
            else:
                s.set_pixel(4, 4, 255, 255, 0)
        else:
            s.set_pixel(0, 4, 255, 0, 255)
    elif right:
        if top:
            if rightOr > topOr:
                s.set_pixel(7, 4, 255, 0, 255)
            elif topOr > rightOr:
                s.set_pixel(4, 0, 255, 0, 255)
            else:
                s.set_pixel(4, 4, 0, 255, 255)
        elif bottom:
            if rightOr > bottomOr:
                s.set_pixel(7, 4, 255, 0, 255)
            elif bottomOr > rightOr:
                s.set_pixel(4, 7, 255, 0, 255)
            else:
                s.set_pixel(4, 4, 255, 255, 0)
        else:
            s.set_pixel(7, 4, 255, 0, 255)
    elif top:
        s.set_pixel(4, 0, 255, 0, 255)
    elif bottom:
        s.set_pixel(4, 7, 255, 0, 255)
    else:
        s.set_pixel(4, 4, 0, 0, 255)
            

while(True):
    check()
    orientation = s.get_orientation()
    s.clear()
    left = False
    right = False
    top = False
    bottom = False
