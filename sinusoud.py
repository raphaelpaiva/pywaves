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
  
  def sample(self, duration, sample_rate):
    t = np.arange(0.0, duration, 1/sample_rate)
    w = 2 * np.pi * self.frequency * t
    samples = self.amplitude * self.func(w + self.phase)
    return samples
