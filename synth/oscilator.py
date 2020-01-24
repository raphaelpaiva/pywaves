#!/usr/bin/python
import math
from .parameter import Parameter, ChoiceParameter
from .waveform import WAVEFORMS

class BaseOscilator(object):
  def __init__(self, name="OSC"):
    super().__init__()
    self.name           = name
    self.parameters     = {}

class Oscilator(BaseOscilator):
  def __init__(self, name='OSC'):
    super().__init__(name=name)
    self.volume = Parameter('volume')
    self.detune = Parameter('detune', min_value=-12, max_value=12)
    self.phase  = Parameter('phase', max_value=2 * math.pi, label_format=lambda x: f"{(x/math.pi):.2f}π")
    self.waveform = ChoiceParameter('waveform', list(WAVEFORMS.values()))
    
    self.parameters = {
      'volume': self.volume,
      'detune': self.detune,
      'phase': self.phase,
      'waveform': self.waveform
    }
  
  def evaluate(self, t, freq):
    detune = self.detune.get()
    phase = self.phase.get()
    amplitude = self.volume.get()
    
    return amplitude * self.waveform.get()(2 * math.pi * (freq + detune) * t + phase)
