import numpy as np

class Sampler(object):
  def __init__(self, sample_rate=44100, sample_size=1024, num_voices=8):
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
    
    return voice_idx
  
  def free_voice(self, voice_idx):
    self.voices[voice_idx] = None

  def create_wave_sample(self, wave, duration, start_time=0.0):
    t = np.arange(start_time, start_time + duration, 1/self.sample_rate)
    w = 2 * np.pi * wave.frequency * t
    rho = wave.phase(t) if callable(wave.phase) else wave.phase
    samples = wave.amplitude * wave.func(w + rho)
    
    return samples

  def sample_waves(self, waves, duration, start_time=0.0):
    samples = []
    
    for wave in waves:
      sample = self.create_wave_sample(wave, duration, start_time)
      samples.append(sample)
    
    return self.mix(samples)

  def get_master(self, duration, start_time=0.0):
    samples = [self.sample_waves(w, duration, start_time) for w in self.voices if w is not None]
    
    return self.mix(samples)

  def mix(self, samples):
      if not samples:
        return []

      final = np.zeros(self.sample_size)
      
      for sample in samples:
        work_sample = sample
        if len(sample) > self.sample_size:
          work_sample = sample[0:self.sample_size] # Hard cut
        
        final = final + work_sample

      return final