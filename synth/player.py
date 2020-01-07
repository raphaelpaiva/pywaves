#!/usr/bin/python

import sounddevice as sd
import numpy

class Player(object):
  def __init__(self, channels=1, audio_format=numpy.float32, volume=0.5):
    self.channels           = channels
    self.format             = audio_format
    self.volume             = volume
    
    self.output_devices     = Player.read_devices()
    self.selected_device_id = sd.default.device[1]

    self.master_sample = None
    self.stream = self.open_stream()

  @classmethod
  def read_devices(self):
    output_devices = {}
    dev_list = sd.query_devices()
    for i in range(len(dev_list)):
      dev = dev_list[i]
      if dev['max_output_channels'] > 0:
        output_devices[i] = dev
  
    return output_devices

  def get_output_device(self):
    return self.output_devices[self.selected_device_id]

  def open_stream(self):
    stream = sd.OutputStream(
      channels= self.channels,
      dtype= self.format,
      device=self.selected_device_id,
      latency='low'
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
