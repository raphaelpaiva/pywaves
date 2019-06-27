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
      on_release = self.onrelease
    )
    self._last_press = None
    self.velocity = 128
  
  def onpress(self, key):
    # BUG: Test this! pressing the same key multiple times
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
    try:
      if key.char in keyboard_note_table:
        note, octave = keyboard_note_table[key.char]
        midi_msg = midi.note_off(note, octave, self.velocity)
        
        self.queue.put(midi_msg)
    except AttributeError:
      self.queue.put(key)
  
  def start(self):
    self.keyboard_listener.start()
  
  def stop(self):
    self.keyboard_listener.stop()
    self.keyboard_listener.join()

if __name__ == "__main__":
  queue = Queue()
  kb = KeyboardInput(queue)

  kb.start()

  item = queue.get()
  while item != keyboard.Key.esc:
    if item is not None:
      print(item)
    
    item = queue.get()

  kb.stop()

    
