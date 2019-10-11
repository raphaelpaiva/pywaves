import os
import sys
import time
import keyboard

from queue import Queue

EVT_KEY          = 'key_'
EVT_KEY_PRESSED  = EVT_KEY + '_pressed'
EVT_KEY_RELEASED = EVT_KEY + '_released'

press_time = 0

class KeyboardInput(object):
  def __init__(self, queue):
    self.queue = queue
    self._last_press = None

  def handle_event(self, event):
    if event.event_type == "down":
      self.onpress(event)
    
    if event.event_type == "up":
      self.onrelease(event)

  def onpress(self, key):
    press_time = time.time()
    if self._last_press == key.name:
      return

    self._last_press = key.name

    self.queue.put(key.name, EVT_KEY_PRESSED, timestamp=press_time)

  def onrelease(self, key):
    release_time = time.time()
    if self._last_press == key.name:
      self._last_press = None

    self.queue.put(key.name, EVT_KEY_RELEASED, timestamp=release_time)

  def start(self): # pragma: no cover
    keyboard.hook(self.handle_event)

  def stop(self): # pragma: no cover
    keyboard.unhook_all()

