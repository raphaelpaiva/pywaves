#!/usr/bin/python
import math
from .parameter import Parameter

class BaseOscilator(object):
  def __init__(self, waveform, name="OSC"):
    super().__init__()
    self.name           = name
    self.waveform  = waveform
    self.parameters     = {}

class Oscilator(BaseOscilator):
  def __init__(self, waveform, name='OSC'):
    super().__init__(waveform, name=name)
    self.volume = Parameter('volume')
    self.detune = Parameter('detune', min_value=-12, max_value=12)
    self.phase  = Parameter('phase', max_value=2 * math.pi, label_format=lambda x: f"{(x/math.pi):.2f}π")
    
    self.parameters = {
      'volume': self.volume,
      'detune': self.detune,
      'phase': self.phase
    }
  
  def evaluate(self, t, freq):
    detune = self.detune.get()
    phase = self.phase.get()
    amplitude = self.volume.get()
    
    return amplitude * self.waveform(2 * math.pi * (freq + detune) * t + phase)
