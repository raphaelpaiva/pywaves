import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import midi
from queue import Queue
from pynput import keyboard

keyboard_note_table = {
  "q": ("E",  4),
  "w": ("F",  4),
  "3": ("F#", 4),
  "e": ("G",  4),
  "4": ("G#", 4),
  "r": ("A",  4),
  "5": ("A#", 4),
  "t": ("B",  4),
  "y": ("C",  5),
  "7": ("C#", 5),
  "u": ("D",  5),
  "8": ("D#", 5),
  "i": ("E",  5),
  "o": ("F",  5),
  "0": ("F#", 5),
  "p": ("G",  5),
  "-": ("G#", 5),
}

class KeyboardInput(object):
  def __init__(self, queue):
    self.queue = queue
    self.keyboard_listener = keyboard.Listener(
      on_press = self.onpress,
      on_release = self.onrelease,
      supress=True
    )
    self._last_press = None
    self.velocity = 128

  def onpress(self, key):
    if self._last_press == key:
      return

    try:
      if key.char in keyboard_note_table:
        note, octave = keyboard_note_table[key.char]
        midi_msg = midi.note_on(note, octave, self.velocity)
        self._last_press = key

        self.queue.put(midi_msg)
    except AttributeError:
      self.queue.put(key)

  def onrelease(self, key):
    if self._last_press == key:
      self._last_press = None

    try:
      if key.char in keyboard_note_table:
        note, octave = keyboard_note_table[key.char]
        midi_msg = midi.note_off(note, octave, self.velocity)

        self.queue.put(midi_msg)
    except AttributeError:
      return

  def start(self): # pragma: no cover
    self.keyboard_listener.start()

  def stop(self): # pragma: no cover
    self.keyboard_listener.stop()
    self.keyboard_listener.join()



