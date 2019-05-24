#!/usr/bin/python

import pyaudio
import numpy

default_config = {
  "channels":   1,
  "read_size":   1024,
  "sample_rate": 44100,
  "duration":    1024 / 44100
}

def play(signal, config=default_config):
  pa = pyaudio.PyAudio()
  stream = pa.open(
    channels = config["channels"],
    format = pyaudio.paFloat32,
    rate=config["sample_rate"],
    output=True
  )

  for t in range(88):
    time = t * config["duration"]
    sample, _ = signal.sample(config["duration"], config["sample_rate"], start_time=time)
    normalized = numpy.interp(sample, (-1, 1), (0, 1)).astype(numpy.float32)
    
    stream.write(normalized.tostring())

  stream.close()
  pa.terminate()
