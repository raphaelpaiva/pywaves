#!/usr/bin/python

import sounddevice as sd
import numpy

class Player(object):
  def __init__(self, channels=1, sample_size=1024, sample_rate=44100, audio_format=numpy.float32, volume=0.5):
    self.channels    = channels
    self.sample_size = sample_size
    self.sample_rate = sample_rate
    self.format      = audio_format
    self.volume      = volume

    self.master_sample = None
    self.stream = self.open_stream()

  def open_stream(self):
    stream = sd.OutputStream(
      channels= self.channels,
      dtype= self.format,
      samplerate =self.sample_rate
    )

    stream.start()

    return stream

  def play_sample(self, sample):
    self.master_sample = sample
    if sample is None or len(sample) == 0:
      return
    
    normalized = self.normalize(sample)

    self.master_sample = normalized
    self.stream.write(normalized)

  def normalize(self, sample):
    return numpy.interp(  # Normalize the sample to range(0, 1)
      sample,
      (-1, 1),            # Original range from Sinewave
      (0, self.volume)    # Target Range: 0 to Volume factor (1 is max)
    ).astype(self.format)

  def set_volume(self, vol):
    self.volume = float(vol)

  def terminate(self):
    self.stream.close()
