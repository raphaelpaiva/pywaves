#!/usr/bin/python

from sinusoud import Sinusoid
from visualizer import visualize

import numpy as np

frequency   = 440   # Hz
sample_rate = 44100 # Samples / Second
read_size   = 1024
duration    = read_size / sample_rate # Seconds

t = np.arange(0.0, duration, 1.0/sample_rate)

signal = Sinusoid(frequency, phase=lambda t: 2*t)

visualize(signal)
