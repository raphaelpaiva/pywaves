#!/usr/bin/python

import time

import matplotlib.pyplot as plt
import numpy as np

from tkinter import TclError
from sinusoud import Sinusoid

default_config = {
  "read_size":   1024,
  "sample_rate": 44100,
  "duration":    1024 / 44100
}

def visualize(signals, config=default_config):
  if isinstance(signals, Sinusoid):
    signals = [signals]

  read_size = config["read_size"]
  duration = config["duration"]
  sample_rate = config["sample_rate"]
  
  t = np.arange(read_size)

  fig, axes = plt.subplots(len(signals))
  if len(signals) == 1:
    axes = [axes]
  
  lines = []
  for ax in axes:
    line, = ax.plot(t, np.random.rand(read_size), '-', lw=2)
    lines.append(line)
    ax.set_ylim(-1,1)
    ax.set_xlim(0, duration)

  plt.show(block=False)
  frame_count = 0
  start_time = time.time()
  sample_frame_number = 0

  while True:
    update_plots(signals, lines, axes, duration, sample_rate, sample_frame_number)

    try:
      fig.canvas.draw()
      fig.canvas.flush_events()
      frame_count += 1
      sample_frame_number += read_size
    except TclError:
      frame_rate = frame_count / (time.time() - start_time)
      print(f"fps: {frame_rate}")
      break

def update_plots(signals, lines, axes, duration, sample_rate, sample_frame_number):
  for i in range(len(signals)):
    signal = signals[i]
    line = lines[i]
    
    sample, t = signal.sample(duration, sample_rate, start_time=sample_frame_number)
    line.set_data(t - sample_frame_number, sample)