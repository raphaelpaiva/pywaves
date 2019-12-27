import numpy as np
from .parameter import Parameter
from scipy import signal

class WaveForm(object):
  def __init__(self, function, parameters={}):
    super().__init__()
    self.function = function
    self.parameters = parameters
  
  def __call__(self, t):
    parameters_kwargs = {k: v.get() if isinstance(v, Parameter) else v for k,v in self.parameters.items()}
    return self.function(t, **parameters_kwargs)


WAVEFORMS = {
  'SINE': WaveForm(np.sin),
  'TRIANGLE': WaveForm(signal.sawtooth, {'width': 0.5}),
  'SAWTOOTH': WaveForm(signal.sawtooth, {'width': Parameter(name='width', min_value=0.0, max_value=1.0, init_value=0.0)})
}