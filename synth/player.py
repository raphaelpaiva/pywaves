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
    max_sample_value = numpy.max(sample)
    ratio = self.volume / max_sample_value
    norm = (ratio * sample).astype(self.format)
    
    return norm

  def set_volume(self, vol):
    self.volume = float(vol)

  def terminate(self):
    self.stream.close()
