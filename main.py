#!/usr/bin/python

from sinusoud import Sinusoid
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

frequency   = 440 #Hz
duration    = 2.0 #Second
sample_rate = 44100 #samples / Second

signal = Sinusoid(frequency)
wave_sample = signal.sample(duration, sample_rate)

plt.plot(np.arange(0.0, duration, 1.0/sample_rate), wave_sample)
plt.show()

wavfile.write('sine.wav', sample_rate, wave_sample)
