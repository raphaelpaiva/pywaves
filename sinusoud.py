#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

class Sinusoid(object):
  def __init__(self, frequency=440, phase=0, amplitude=1.0, func=np.sin):
    self.amplitude = amplitude
    self.frequency = frequency
    self.phase = phase
    self.func = func

  def __str__(self):
    return f"{self.amplitude} * {self.func.__name__}(2 * PI * {self.frequency} + {self.phase})"
  
  def sample(self, duration, sample_rate, start_time=0.0):
    t = np.arange(start_time, start_time + duration, 1/sample_rate)
    w = 2 * np.pi * self.frequency * t
    rho = self.phase(t) if callable(self.phase) else self.phase
    samples = self.amplitude * self.func(w + rho)
    
    return samples, t
