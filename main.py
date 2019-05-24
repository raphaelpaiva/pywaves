#!/usr/bin/python

from sinusoud import Sinusoid
from visualizer import visualize
from player import play

import numpy as np

frequency   = 990   # Hz
sample_rate = 44100 # Samples / Second
read_size   = 1024
duration    = read_size / sample_rate # Seconds

t = np.arange(0.0, duration, 1.0/sample_rate)

signals = [
  Sinusoid(frequency),
  Sinusoid(frequency, phase=1)
]

frame_rate = visualize(signals)
print(f"fps: {frame_rate}")
play(signals[0])