#!/usr/bin/python

import pyaudio
import numpy

class Player(object):
  def __init__(self, channels=1, sample_size=1024, sample_rate=44100, audio_format=pyaudio.paFloat32, volume=0.5):
    self.channels    = channels
    self.sample_size = sample_size
    self.sample_rate = sample_rate
    self.format      = audio_format
    self.volume      = volume
    self.pyaudio     = pyaudio.PyAudio()

    self.stream = self.open_stream()

  def open_stream(self):
    stream = self.pyaudio.open(
      channels = self.channels,
      format = self.format,
      rate=self.sample_rate,
      output=True
    )

    return stream

  def mix(self, samples):
    if not samples:
      return []
    
    normalized_samples = numpy.zeros(self.sample_size)
    
    for sample in samples:
      work_sample = sample
      if len(sample) > self.sample_size:
        work_sample = sample[0:self.sample_size] # Hard cut
      
      norm_sample = self.normalize(work_sample)
      normalized_samples = normalized_samples + norm_sample
    
    return normalized_samples

  def play_sample(self, sample):
    normalized = self.normalize(sample)
    
    self.stream.write(normalized.tostring())

  def normalize(self, sample):
    return numpy.interp(  # Normalize the sample to range(0, 1)
      sample,
      (-1, 1),            # Original range from Sinewave
      (0, self.volume)    # Target Range: 0 to Volume factor (1 is max)
    ).astype(numpy.float32)

  def set_volume(self, vol):
    self.volume = float(vol)

  def terminate(self):
    self.stream.close()
    self.pyaudio.terminate()
