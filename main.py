import adafruit_dotstar
import board
from digitalio import DigitalInOut,Direction,Pull
from time import sleep, monotonic

from adafruit_hid.gamepad import Gamepad
from mode import Mode

def hex2rgb(hexcode):
    #added 1 to all for #
    red = int("0x"+hexcode[1:3], 16)
    green = int("0x"+hexcode[3:5], 16)
    blue = int("0x"+hexcode[5:7], 16)
    rgb = (red, green, blue)
    return rgb

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

gp = Gamepad()

import settings

print(settings.modes)

modeDelay = settings.modeDelay
repeatDelay = settings.repeatDelay

modeSwitchCode = 0x0

for num in settings.modeSwitches:
    modeSwitchCode |= (1 << num)

modeNum = 0
currentMode = settings.modes[modeNum]

modeColor=hex2rgb(currentMode.color)

def dpadMap(s):
    return int((s + 1) * (254) / (2))

def handleLongPress(switchCode):
    global modeColor
    global modeNum
    global currentMode
#################
pins = [
        DigitalInOut(board.D0),
        DigitalInOut(board.D1),
        DigitalInOut(board.D2),
        DigitalInOut(board.D3),
        DigitalInOut(board.D4)
        ]
for p in pins:
    p.direction = Direction.INPUT
    p.pull = Pull.UP

lastCode = 0
lastModifier = 0
repeat = 0
codeStartTime = monotonic()

while(True):
    num = 0
    sw = [0,0,0,0,0]
    switchCode = 0x00
    readTime = monotonic()
    for p in pins:
        num = num + 1
        if(p.value == False):
            switchCode |= (1 << num)
    if (switchCode != 0):
        lastSwitchCode = switchCode
        for i in range(num):
            sw[num-i-1]=lastSwitchCode/pow(2,num-i)
            lastSwitchCode= lastSwitchCode%pow(2,num-i)
            if (lastSwitchCode in currentMode.actions):
                a = currentMode.actions[lastSwitchCode]
                if a[0] == Mode.BUTTON_PRESS:
                    (actionType, buttonNum) = a
                    if type(buttonNum) is int:
                        print("Button=",buttonNum)
                        gp.press_buttons(buttonNum)
                    else:
                        for b in buttonNum:
                            print("Button=",b)
                            gp.press_buttons(b)
                elif a[0] == Mode.DPAD_MOVE:
                    (actionType, x, y) = a
                    print("x=",x,",y=",y)
                    gp.move_joysticks(dpadMap(x),dpadMap(-y))
            lastSwitchCode= lastSwitchCode%pow(2,num-i)
        if (switchCode != lastCode):
            print("NewCode")
            lastCode = switchCode
            codeStartTime = readTime
        else:
            if (readTime > (codeStartTime + modeDelay)):
                print("longPress")
                if (switchCode == modeSwitchCode):
                    numOfModes = len(settings.modes)
                    modeNum = (modeNum + 1) % numOfModes
                    currentMode = settings.modes[modeNum]
                    modeColor=hex2rgb(currentMode.color)
                    dot[0]=modeColor
                codeStartTime = readTime
    else:
        #print("Release")
        gp.release_all_buttons()
        gp.move_joysticks(127,127)
    lastCode = switchCode
    sleep(repeatDelay)
    dot[0]=modeColor