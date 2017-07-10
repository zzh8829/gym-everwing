import gym
from gym import error, spaces, utils
from gym.utils import seeding

import deep_capture
import os
import numpy as np
import pygame
from pygame.locals import *

import Quartz
import AppKit
from pynput import keyboard

import time

ACTIONS = {
  0 : "NOOP",
  1 : "FIRE",
  2 : "UP",
  3 : "RIGHT",
  4 : "LEFT",
  5 : "DOWN",
}

# hardcoded game window location
GAME_RECT = [252, 173, 456, 810]

DTM = GAME_RECT[2] * 0.5, GAME_RECT[3] * 0.70

def mouseLocation():
    loc = AppKit.NSEvent.mouseLocation()
    return int(loc.x), int(Quartz.CGDisplayPixelsHigh(0) - loc.y)

def mouseTo(x,y):
    x += GAME_RECT[0]
    y += GAME_RECT[1]

    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

def mouseDown():
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, mouseLocation(), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

def mouseUp():
    mouseEvent = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, mouseLocation(), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouseEvent)

SCREEN_SIZE = GAME_RECT[2],GAME_RECT[3]
SCREEN_FLAG = DOUBLEBUF|HWSURFACE

class Viewer:
  def __init__(self):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (GAME_RECT[0] + GAME_RECT[2] * 1.5,GAME_RECT[1])

    pygame.init()
    pygame.display.set_caption("Deep EverWing")
    self.screen = pygame.display.set_mode(SCREEN_SIZE, SCREEN_FLAG)
    self.font = pygame.font.SysFont("Courier New",15)
    self.clock = pygame.time.Clock()

  def render(self, img):
    self.clock.tick(60)

    for event in pygame.event.get():
      if event.type == QUIT:
          running = False

    frame_sf = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
    self.screen.blit(frame_sf, (0, 0))

    fps_sf = self.font.render("FPS: %.2f"%self.clock.get_fps(), True, (255, 0, 0))
    self.screen.blit(fps_sf, (0,0))

    pygame.display.flip()

  def __del__(self):
    pygame.quit()

class EverWingEnv(gym.Env):
  metadata = {
    'render.modes': ['human', 'rgb'],
    'mouse.speed': 30
  }

  def __init__(self):
    self.action_space = spaces.Discrete(len(ACTIONS))

    self.dc = deep_capture.create_display_capture()
    self.dc.init()
    self.dc.start()

    self.viewer = None

  def __del__(self):
    self.dc.stop()

  def get_action_space():
    return gym.spaces.discrete.Discrete(6)

  def _step(self, action):
    if action in [0, 2, 4]:
      mouseTo(DTM[0], DTM[1])
      mouseDown()
      mouseTo(DTM[0] - self.metadata['mouse.speed'], DTM[1])
      mouseUp()
    elif action in [1, 3, 5]:
      mouseTo(DTM[0], DTM[1])
      mouseDown()
      mouseTo(DTM[0] + self.metadata['mouse.speed'], DTM[1])
      mouseUp()

    time_lapsed = time.clock() - self.start_time

    # BGRA to RGB
    self.obs = self.dc.capture(GAME_RECT)[:,:,[2,1,0]]
    reward = time_lapsed
    done = time_lapsed > 5
    info = None
    return self.obs, reward, done, info

  def _reset(self):
    mouseTo(DTM[0], DTM[1])
    mouseDown()
    mouseUp()

    self.start_time = time.clock()

    self.obs = self.dc.capture(GAME_RECT)[:,:,[2,1,0]]
    return self.obs

  def _render(self, mode='human', close=False):
    if close:
      return

    if mode != 'human':
      if not self.viewer:
        self.viewer = Viewer()

      self.viewer.render(self.obs)

    return self.obs


