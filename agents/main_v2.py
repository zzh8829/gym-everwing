import os
import sys
import time
import matplotlib.pyplot as plt

import deep_capture

import numpy as np
import cv2
import pygame
from pygame.locals import *

from pynput import keyboard
import Quartz
import AppKit

CAPTURE_ORIGIN = [252, 173]
CAPTURE_SIZE = [456, 810]

def mouseLocation():
    loc = AppKit.NSEvent.mouseLocation()
    return int(loc.x), int(Quartz.CGDisplayPixelsHigh(0) - loc.y)

def mouseTo(x,y):
    x += CAPTURE_ORIGIN[0]
    y += CAPTURE_ORIGIN[1]

    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

def mouseDown():
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, mouseLocation(), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

def mouseUp():
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, mouseLocation(), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

w, h = CAPTURE_SIZE

moves = np.linspace(-w/3, w/3, 30)
moves = np.concatenate((moves, moves[::-1]))

dtm_w, dtm_h = w * 0.5, h * 0.70
mouseTo(dtm_w, dtm_h)
time.sleep(0.01)
mouseDown()
time.sleep(0.01)
mouseUp()

mi = len(moves)//2

cnt = 0
def linear_movement():
    global mi, cnt
    mi = (mi + 1)%len(moves)
    cnt += 1

    if cnt % (60 * 10) == 0:
        mouseTo(w * 0.25, h * 0.85)
        time.sleep(0.01)
        mouseDown()
        time.sleep(0.01)
        mouseUp()
        time.sleep(0.01)

        mouseTo(dtm_w, dtm_h)
        time.sleep(0.01)
        mouseDown()
        time.sleep(0.01)
        mouseUp()

        mi = len(moves)//2

    m = moves[mi]
    mouseDown()
    mouseTo(dtm_w + m, dtm_h)
    mouseUp()

running = True
def main(argv):
    global running

    SCREEN_SIZE = CAPTURE_SIZE
    SCREEN_FLAG = DOUBLEBUF|HWSURFACE|RESIZABLE
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1000,150)

    dc = deep_capture.create_display_capture()
    dc.init()
    dc.start()

    def on_press(key):
        global running
        if str(key) == 'Key.cmd':
            running = False

    listener = keyboard.Listener(on_press)
    listener.start()

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAG)
    pygame.display.set_caption("Deep EverWing")
    font = pygame.font.SysFont("Courier New",15)
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                SCREEN_SIZE = event.dict['size']
                screen = pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAG)
            elif event.type == KEYDOWN:
                if event.unicode == "D":
                    detect = not detect

        linear_movement()

        screen.fill((0,0,0))

        frame = dc.capture((CAPTURE_ORIGIN[0], CAPTURE_ORIGIN[1], CAPTURE_SIZE[0], CAPTURE_SIZE[1]))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        img = frame

        frame_sf = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
        frame_sf = pygame.transform.scale(frame_sf, SCREEN_SIZE)

        screen.blit(frame_sf, (0, 0))

        fps_sf = font.render("FPS: %.2f"%clock.get_fps(), True, (255, 0, 0))
        screen.blit(fps_sf, (0,0))

        pygame.display.flip()

    dc.stop()
    listener.stop()
    pygame.quit()

if __name__=='__main__':
    main(sys.argv)
