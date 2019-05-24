#!/usr/bin/python

from sinusoud import Sinusoid

class Oscilator(object):
  def __init__(self, wave, name="OSC", volume=1.0):
    self.name           = name
    self.wave           = wave
    self.volume         = volume
    self.wave.amplitude = volume
  
  def set_frequency(self, freq):
    self.wave.frequency = float(freq)
  
  def set_volume(self, vol):
    self.volume         = float(vol)
    self.wave.amplitude = self.volume