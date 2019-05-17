#!/usr/bin/python

import time

import matplotlib.pyplot as plt
import numpy as np

from tkinter import TclError

default_config = {
  "read_size":   1024,
  "sample_rate": 44100,
  "duration":    1024 / 44100
}

def visualize(signal, config=default_config):
  read_size = config["read_size"]
  duration = config["duration"]
  sample_rate = config["sample_rate"]
  
  t = np.arange(read_size)

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