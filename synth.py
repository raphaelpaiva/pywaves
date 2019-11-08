import threading
import copy
from event_queue import (EventQueue, Event)
import input
from input import (KeyboardInput, EVT_KEY, EVT_KEY_PRESSED, EVT_KEY_RELEASED)
import midi
import time
import numpy as np

from sinusoud import (Sinusoid, Triangle)
from oscilator import Oscilator
from player import Player
from sampler import Sampler

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

class Synth(object):
  def __init__(self):
    self._init_input()
    self._init_generator()
    self._init_sound_engine()
    
    self.note_voice = {}

  def _init_input(self):
    self.event_queue = EventQueue()
    self.input = KeyboardInput(self.event_queue)

    self.input.start()

  def _init_generator(self):
    self.oscilators = [
      Oscilator(name="Sine", wave=Sinusoid(frequency=303.04429))
    ]

  def _init_sound_engine(self):
    self.player        = Player()
    self.sampler       = Sampler()
    self.player_thread = threading.Thread(target=self._continuous_play)

    self.stop = False
    self.player_thread.start()

  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration

      master = self.sampler.get_master(duration, time)
      
      master_time = np.arange(len(master))
      master_limits = (0, len(master_time))
      
      self.player.play_sample(master)

      t += 1

  def terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()

    self.input.stop()

  def _evt_note_on(self, item):
    sample_size = self.player.sample_size
    sample_rate = self.player.sample_rate
    duration    = sample_size / sample_rate
    
    note_number = item.data1
    freq = midi.midi_number_to_freq(note_number)
    for osc in self.oscilators:
      osc.set_frequency(freq)
    
    waves = [copy.copy(o.wave) for o in self.oscilators]
    voice_index = self.sampler.allocate_voice(waves)

    self.note_voice[note_number] = voice_index
  
  def _evt_note_off(self, item):
    note_number = item.data1
    voice_idx = self.note_voice[note_number]
    self.sampler.free_voice(voice_idx)

  def process_queue(self):
    while True:
      event = self.event_queue.get()

      if event is None:
        continue
      
      if event.item == 'esc':
        break
      
      item = event.item

      if event.type == midi.EVT_MIDI:
        if item.status == midi.ST_NOTE_ON:
          self._evt_note_on(item)
        
        if item.status == midi.ST_NOTE_OFF:
          self._evt_note_off(item)

      if event.type.startswith(EVT_KEY):
        if item not in keyboard_note_table:
          continue

        note, octave = keyboard_note_table[item]
        
        if event.type == EVT_KEY_PRESSED:
          new_event = Event(
            midi.note_on(note, octave, 127),
            midi.EVT_MIDI,
            ancestor=event,
            timestamp=time.time()
          )

        if event.type == EVT_KEY_RELEASED:
          new_event = Event(
            midi.note_off(note, octave, 127),
            midi.EVT_MIDI,
            ancestor=event,
            timestamp=time.time()
          )

        self.event_queue.put(new_event)

