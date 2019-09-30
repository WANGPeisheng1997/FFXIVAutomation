import pyautogui
import sys
import time
from fuzzy_match import fuzzy_similarity, fuzzy_images_match
import PIL
pyautogui.FAILSAFE = True
print('Press Ctrl-C to quit.')
time.sleep(2)

from chocobo_racing import recognize_exp, recognize_jdb

try:
    while True:

        res = pyautogui.locateOnScreen("reward.png")
        print(res)
        # res = pyautogui.locateOnScreen("digit7.png")
        # print(res)
        # res = pyautogui.locateOnScreen("digit2.png")
        # print(res)
        d = recognize_exp(res)
        print(d)
        d = recognize_jdb(res)
        print(d)


except KeyboardInterrupt:
    print('\n')

# Box(left=801, top=475, width=34, height=14) r
# Box(left=777, top=498, width=6, height=18) 5
# Box(left=867, top=498, width=6, height=18) 8


# bisaijieguo 796 429
# ABC 787(+8+8) 497
# DEF 869(+8+8) 497
