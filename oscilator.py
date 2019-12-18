#!/usr/bin/python
import math

from sinusoud import Sinusoid

class BaseOscilator(object):
  def __init__(self, wave_function, name="OSC"):
    super().__init__()
    self.name           = name
    self.wave_function  = wave_function
    self.parameters     = {}

class Oscilator(BaseOscilator):
  def __init__(self, wave_function, name='OSC'):
    super().__init__(wave_function, name=name)
    self.parameters = {
      'volume': Parameter('volume'),
      'detune': Parameter('detune', min_value=-12, max_value=12),
      'phase': Parameter('phase', max_value=2 * math.pi, label_format=lambda x: f"{(x/math.pi):.2f}π"),
    }
  
  def evaluate(self, t, freq):
    detune = self.parameters['detune'].get()
    phase = self.parameters['phase'].get()
    amplitude = self.parameters['volume'].get()
    
    return amplitude * self.wave_function(2 * math.pi * (freq + detune) * t + phase)
class Parameter(object):
  """ A parameter[name, relative_value]. relative_value is a float between 0 and 1 where 0 is minimum and 1 is maximum value. For absolute values (defined by min_value and max_value), use get(). """
  def __init__(self, name, min_value=0.0, max_value=1.0, init_value=0.5, label_format=None):
    super().__init__()
    
    self.name = name
    
    self.relative_value = init_value
    self.max_value = max_value
    self.min_value = min_value
    self.label_format = label_format

  def get(self):
    """ Returns the absolute value of this parameter, based on the minimum and maximum values. """
    return self.relative_value * (self.max_value - self.min_value) + self.min_value
  
  def get_relative(self):
    return self.relative_value

  def set_relative(self, new_value):
    """ Sets the relative value [0,1] where 0 is minumum and 1 is maximum. """
    if new_value < 0.0:
      self.relative_value = 0.0
    elif new_value > 1.0:
      self.relative_value = 1.0
    else:
      self.value = new_value