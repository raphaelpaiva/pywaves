import os
import sys
import time

from queue import Queue
from pynput import keyboard

EVT_KEY          = 'key_'
EVT_KEY_PRESSED  = EVT_KEY + '_pressed'
EVT_KEY_RELEASED = EVT_KEY + '_released'

press_time = 0

class KeyboardInput(object):
  def __init__(self, queue):
    self.queue = queue
    self.keyboard_listener = keyboard.Listener(
      on_press = self.onpress,
      on_release = self.onrelease,
      supress=True
    )
    self._last_press = None

  def onpress(self, key):
    press_time = time.time()
    if self._last_press == key:
      return

    if hasattr(key, 'char'):
      self._last_press = key
      self.queue.put(key.char, EVT_KEY_PRESSED, timestamp=press_time)
    else:
      self.queue.put(f"<{key.name}>", EVT_KEY_PRESSED, timestamp=press_time)

  def onrelease(self, key):
    release_time = time.time()
    if self._last_press == key:
      self._last_press = None

    try:
      self.queue.put(key.char, EVT_KEY_RELEASED, timestamp=release_time)
    
    except AttributeError:
      return

  def start(self): # pragma: no cover
    self.keyboard_listener.start()

  def stop(self): # pragma: no cover
    self.keyboard_listener.stop()
    self.keyboard_listener.join()



