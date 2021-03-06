import numpy as np
import logging

LOGGER_NAME = 'Sampler'

class Sampler(object):
  def __init__(self, sample_rate=44100, sample_size=1024, num_voices=8, log=None):
    self.log = log.getChild(LOGGER_NAME) if log else logging.getLogger(LOGGER_NAME)
    
    self.num_voices = num_voices
    self.sample_size = sample_size
    self.sample_rate = sample_rate
    self.voices = [None] * num_voices

  def _get_first_avilable_voice(self):
    for i in range(self.num_voices):
      if self.voices[i] is None:
        return i
    
    return -1

  def allocate_voice(self, payload):
    voice_idx = self._get_first_avilable_voice()
    self.voices[voice_idx] = payload
    
    self.log.debug(f'Allocating voice {voice_idx} with {payload}')
    return voice_idx
  
  def free_voice(self, voice_idx):
    self.log.debug(f'Freeing voice {voice_idx}')
    self.voices[voice_idx] = None
    self.log.debug(f'Voice Status: {self.voices}')

  def sample_waves(self, payload, duration, start_time=0.0):
    samples = []
    oscilators, freq = payload
    
    for osc in oscilators:
      t = np.arange(start_time, start_time + duration, 1/self.sample_rate)
      sample = osc.evaluate(t, freq)
      samples.append(sample)
    
    return self.mix(samples)

  def get_master(self, duration, start_time=0.0):
    samples = [self.sample_waves(o, duration, start_time) for o in self.voices if o is not None]
    
    return self.mix(samples)

  def mix(self, samples):
      if not samples:
        return []

      self.log.debug(f'Voice Status: {self.voices}')
      self.log.debug(f'Mixing {len(samples)} samples')

      final = np.zeros(self.sample_size)
      
      for sample in samples:
        work_sample = sample
        if len(sample) > self.sample_size:
          work_sample = sample[0:self.sample_size] # Hard cut
        
        final = final + work_sample

      return final