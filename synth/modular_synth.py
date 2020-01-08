import time
import queue

from .oscilator import Oscilator
from .module import ThreadModule
from .sampler import Sampler
from .waveform import WAVEFORMS
from .player import Player


class ModularSynth(object):
  def __init__(self):
    super().__init__()
    
    self.sampler = SamplerModule('Sampler')
    self.output = SoundOutputModule('Output')
    
    self.sampler.output.connect(self.output)

    self.modules = {
      self.sampler.name: self.sampler,
      self.output.name: self.output
    }
  
  def start(self):
    for m in self.modules.values():
      m.start()

  def stop(self):
    for m in self.modules.values():
      m.stop()

class SamplerModule(ThreadModule):
  def __init__(self, name: str):
    super().__init__(name)
    self.sampler = Sampler()
    self.sampler.allocate_voice(([
      Oscilator(name="Sinusoid 1", waveform=WAVEFORMS['SINE']),
      Oscilator(name="Sinusoid 1", waveform=WAVEFORMS['SQUARE'])
    ], 220.0))

  def run(self):
    t = 0
    while not self.do_stop:
      sample_size = self.sampler.sample_size
      sample_rate = self.sampler.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration

      master = self.sampler.get_master(duration, time)

      if len(master) > 0:
        self.output.put(master)
        t += 1
      else:
        t = 0

class SoundOutputModule(ThreadModule):
  def __init__(self, name: str):
    super().__init__(name)
    self.player = Player()
  
  def run(self):
    while not self.do_stop:
      try:
        master = self.input.get(timeout=1)
        self.player.play_sample(master)
      except queue.Empty: pass
