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

    self.sampling_lock = threading.Condition()
    
    self._init_queue()
    self._init_generator()
    self._init_sound_engine()
    
    self.note_voice = {}

  def _init_queue(self):
    self.input_queue = EventQueue()

  def _init_generator(self):
    self.oscilators = [
      Oscilator(name="Sinusoid 1", wave=Sinusoid()),
      Oscilator(name="Triangle 1", wave=Triangle()),
    ]

  def _init_sound_engine(self):
    self.player        = Player()
    self.sampler       = Sampler(log=self.log)
    self.output_queue  = EventQueue(2)
    self.stop           = False
    
    self.player_thread  = threading.Thread(name='SyPlayerT', target=self._continuous_play)
    self.sampler_thread = threading.Thread(name='SySamplerT',target=self._continuous_sample)
    self.queue_thread   = threading.Thread(name='SyQueueT', target=self.process_queue)

    
    self.player_thread.start()
    self.sampler_thread.start()
    self.queue_thread.start()

  def _continuous_sample(self):
    t = 0
    while not self.stop:
      sample_size = self.sampler.sample_size
      sample_rate = self.sampler.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration

      master = self.sampler.get_master(duration, time)

      if len(master) > 0:
        self.log.debug(f'Putting {len(master)}')
        self.output_queue.put(master, 'sample')
        t += 1
      else:
        t = 0
        with self.sampling_lock:
          self.sampling_lock.wait()
    
    self.log.debug("Exited sampler loop.")

  def _continuous_play(self):
    while not self.stop:
      try:
        event = self.output_queue.get(timeout=1)
        master = event.item
        self.log.debug(f'Sample Queue Size {self.output_queue.qsize()}')
        self.player.play_sample(master)
      except Exception as e: pass

    self.log.debug("Exited player loop.")

  def terminate(self):
    self.log.debug('Terminating Synth...')
    self.stop = True
    
    self.log.debug('Stopping Player Thread...')
    self.player_thread.join()
    
    self.log.debug('Stopping Sampler Thread...')
    with self.sampling_lock:
      self.sampling_lock.notify()
    self.sampler_thread.join()

    self.log.debug('Terminating Player...')
    self.player.terminate()
    
    if threading.get_ident() != self.queue_thread.ident:
      self.log.debug('Stopping Event Queue Thread...')
      self.input_queue.put(TERMINATE_EVT)
      self.queue_thread.join()

  def _evt_note_on(self, item):
    note_number = item.data1
    freq = midi.midi_number_to_freq(note_number)
    
    waves = [o.wave for o in self.oscilators]
    voice_index = self.sampler.allocate_voice((waves, freq))
    with self.sampling_lock:
      self.sampling_lock.notify()

    self.note_voice[note_number] = voice_index
    self.log.debug(f'Processed note_on event: #{note_number}, {freq}Hz, Voice {voice_index}')
  
  def _evt_note_off(self, item):
    note_number = item.data1
    voice_idx = self.note_voice[note_number]
    self.sampler.free_voice(voice_idx)
    self.log.debug(f'Processed note_off event: #{note_number}, Voice {voice_idx}')

  def _evt_syscom(self, item):
    if item.data1 == 0 and item.data2 == 0:
      self.log.debug('Got syscom_exit event.')
      self.terminate()

  def process_queue(self):
    while not self.stop:
      event = self.input_queue.get() # Blocking
      self.log.debug(f'Got event {event}')

      item = event.item

      if event.type == midi.EVT_MIDI:
        if item.status == midi.ST_SYS_COM:
          self._evt_syscom(item)
        if item.status == midi.ST_NOTE_ON:
          self._evt_note_on(item)
        if item.status == midi.ST_NOTE_OFF:
          self._evt_note_off(item)
    
    self.log.debug("Exited Event Queue loop.")
