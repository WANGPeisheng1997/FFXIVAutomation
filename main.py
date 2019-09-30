import pyautogui
import sys
import time
pyautogui.FAILSAFE = True
print('Press Ctrl-C to quit.')
time.sleep(2)

try:
    while True:
        res = pyautogui.locateOnScreen("search3.png")
        print(res)
        print(pyautogui.pixel(res[0]+20, res[1]+260))
except KeyboardInterrupt:
    print('\n')

