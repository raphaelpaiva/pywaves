#!/usr/bin/python

import pyaudio
import numpy

default_config = {
  "channels":   1,
  "read_size":   1024,
  "sample_rate": 44100,
  "duration":    1024 / 44100,
  "format": pyaudio.paFloat32,
  "volume": 0.5
}

def play(signal, config=default_config):
  play_sinusoid(signal, config)

def play_sinusoid(signal, config=default_config):
  pa = pyaudio.PyAudio()
  stream = pa.open(
    channels = config["channels"],
    format = config["format"],
    rate=config["sample_rate"],
    output=True
  )

  for t in range(88):
    time = t * config["duration"]
    sample, _ = signal.sample(config["duration"], config["sample_rate"], start_time=time)
    normalized = numpy.interp(sample, (-1, 1), (0, config["volume"])).astype(numpy.float32)
    
    stream.write(normalized.tostring())

  stream.close()
  pa.terminate()

class Player(object):
  def __init__(self, channels=1, sample_size=1024, sample_rate=44100, audio_format=pyaudio.paFloat32, volume=0.5):
    self.channels = channels
    self.read_size = sample_size
    self.sample_rate = sample_rate
    self.format = audio_format
    self.volume = volume
    self.pyaudio = pyaudio.PyAudio()

    self.stream = self.open_stream()

  def open_stream(self):
    stream = self.pyaudio.open(
      channels = self.channels,
      format = self.format,
      rate=self.sample_rate,
      output=True
    )

    return stream

  def play_sample(self, sample):
    normalized = numpy.interp(  # Normalize the sample to range(0, 1)
      sample,
      (-1, 1),                  # Original range from Sinewave
      (0, self.volume)          # Target Range: 0 to Volume factor (1 is max)
    ).astype(numpy.float32)
    
    self.stream.write(normalized.tostring())

  def terminate(self):
    self.stream.close()
    self.pyaudio.terminate()
