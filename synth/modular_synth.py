import time
import queue

from .oscilator import Oscilator
from .module import Module, ThreadModule
from .sampler import Sampler
from .waveform import WAVEFORMS
from .player import Player

class ModularSynth(object):
  def __init__(self):
    super().__init__()
    
    self.event_input = queue.Queue()
    self.sampler = SamplerModule('Sampler')
    self.output = SoundOutputModule('Output')
    self.generator = GeneratorModule('Generator')
    
    self.sampler.output.connect(self.output)

    self.modules = {
      self.sampler.name: self.sampler,
      self.output.name: self.output,
      self.generator.name: self.generator
    }

    self._commands = {
      'play': self._play,
      'add':  self._add_osc,
      'set':  self._set
    }

  def _play(self, freq):
    self.sampler.sampler.allocate_voice((self.generator.get_oscilators(), freq))
  
  def _add_osc(self, osc_name):
    self.generator.add_osc(
      Oscilator(name=osc_name)
    )

  def _set(self, osc_name: str, param_name: str, value: float):
    self.generator._oscilators[osc_name].parameters[param_name].set_relative(value)

  def input(self, cmd):
    self.event_input.put(cmd)

  def process(self):
    try:
      while not self.event_input.empty():
        cmd = self.event_input.get(block=False)
        self._commands[cmd.name](*cmd.get_params())
    except queue.Empty: pass


  def start(self):
    for m in self.modules.values():
      m.start()

  def stop(self):
    for m in self.modules.values():
      m.stop()

class Command(object):
  def __init__(self, name: str, *args):
    super().__init__()
    self.name = name
    self.params = args

  def get_params(self):
    return self.params
  
  def __str__(self):
    return f'{self.name} {self.params}'

class SamplerModule(ThreadModule):
  def __init__(self, name: str):
    super().__init__(name)
    self.sampler = Sampler()

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

class GeneratorModule(Module):
  def __init__(self, name: str):
    super().__init__(name)
    self._oscilators = {}

  def run(self): pass

  def add_osc(self, osc: Oscilator):
    self._oscilators[osc.name] = osc
  
  def rem_osc(self, osc):
    self._oscilators.pop(osc.name, None)
  
  def get_oscilators(self):
    return self._oscilators.values()