import time
import pyautogui

import Quartz

def moveTo(x,y):
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

w, h = pyautogui.size()

bw, bh = w * 0.5, h * 0.8

moves = list(range(-150,150,10)) + list(range(150,-150,-10))

moveTo(bw, bh)
pyautogui.click();

while True:
    moveTo(bw - 100, bh)
    pyautogui.click();
    time.sleep(0.001)
    moveTo(bw, bh * 0.8)
    pyautogui.click();
    time.sleep(0.001)

    moveTo(bw, bh * 0.9)
    pyautogui.mouseDown();
    for i in range(10):
        for m in moves:
            moveTo(bw + m, bh * 0.9)
            time.sleep(0.008)
    pyautogui.mouseUp()
