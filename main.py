#!/usr/bin/python

import time
from sinusoud import Sinusoid

import matplotlib.pyplot as plt
import numpy as np

from tkinter import TclError

frequency   = 440   # Hz
sample_rate = 44100 # Samples / Second
read_size   = 1024
duration    = read_size / sample_rate # Seconds

t = np.arange(0.0, duration, 1.0/sample_rate)

signal = Sinusoid(frequency, phase=lambda t: 2*t)

fig, ax = plt.subplots(1)
line, = ax.plot(t, np.random.rand(read_size), '-', lw=2)

plt.show(block=False)

frame_count = 0
start_time = time.time()
sample_frame_number = 0
ax.set_ylim(-1,1)
while True:
  sample, t = signal.sample(duration, sample_rate, start_time=sample_frame_number)
  line.set_data(t, sample)
  ax.set_xlim(sample_frame_number, duration + sample_frame_number)
  frame_count += 1
  sample_frame_number += read_size

  try:
    fig.canvas.draw()
    fig.canvas.flush_events()
  except TclError:
    frame_rate = frame_count / (time.time() - start_time)
    print(f"fps: {frame_rate}")
    break

