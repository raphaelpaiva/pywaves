import threading
import copy
from event_queue import (EventQueue, Event)
import midi
import time
import numpy as np
import logging

from sinusoud import (Sinusoid, Triangle)
from oscilator import Oscilator
from player import Player
from sampler import Sampler

LOGGER_NAME = 'Synth'

TERMINATE_EVT = Event(midi.EVT_MIDI, midi.SYSCOM_EXIT)

class Synth(object):
  def __init__(self, log=None):
    self.log = log.getChild(LOGGER_NAME) if log else logging.getLogger(LOGGER_NAME)

    self._init_queue()
    self._init_generator()
    self._init_sound_engine()
    
    self.note_voice = {}

  def _init_queue(self):
    self.event_queue = EventQueue()

  def _init_generator(self):
    self.oscilators = [
      Oscilator(name="Sinusoid", wave=Sinusoid()),
    ]

  def _init_sound_engine(self):
    self.player        = Player()
    self.sampler       = Sampler()
    self.player_thread = threading.Thread(target=self._continuous_play)
    self.queue_thread = threading.Thread(target=self.process_queue)

    self.stop = False
    
    self.player_thread.start()
    self.queue_thread.start()

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
    
    self.log.debug("Exited player loop.")

  def terminate(self):
    self.log.debug('Terminating Synth...')
    self.stop = True
    
    self.log.debug('Stopping Player Thread...')
    self.player_thread.join()
    
    self.log.debug('Terminating Player...')
    self.player.terminate()
    
    if threading.get_ident() != self.queue_thread.ident:
      self.log.debug('Stopping Event Queue Thread...')
      self.event_queue.put(TERMINATE_EVT)
      self.queue_thread.join()

  def _evt_note_on(self, item):
    sample_size = self.player.sample_size
    sample_rate = self.player.sample_rate
    duration    = sample_size / sample_rate
    
    note_number = item.data1
    freq = midi.midi_number_to_freq(note_number)
    for osc in self.oscilators:
      osc.set_frequency(freq)
    
    waves = [o.wave for o in self.oscilators]
    voice_index = self.sampler.allocate_voice(waves)

    self.note_voice[note_number] = voice_index
  
  def _evt_note_off(self, item):
    note_number = item.data1
    voice_idx = self.note_voice[note_number]
    self.sampler.free_voice(voice_idx)

  def _evt_syscom(self, item):
    if item.data1 == 0 and item.data2 == 0:
      self.log.debug('Got syscom_exit event.')
      self.terminate()

  def process_queue(self):
    while not self.stop:
      event = self.event_queue.get() # Blocking

      item = event.item

      if event.type == midi.EVT_MIDI:
        if item.status == midi.ST_SYS_COM:
          self._evt_syscom(item)
        if item.status == midi.ST_NOTE_ON:
          self._evt_note_on(item)
        if item.status == midi.ST_NOTE_OFF:
          self._evt_note_off(item)
    
    self.log.debug("Exited Event Queue loop.")
