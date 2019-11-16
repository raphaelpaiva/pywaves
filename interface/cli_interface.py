class CLInterface(object):
  def __init__(self, synth, **kwargs):
    self.synth = synth
  
  def start(self):
    print("JustASynth!")
    print(f"""
    Channels:    {self.synth.player.channels}
    Sample Size: {self.synth.player.sample_size}
    Sample Rate: {self.synth.player.sample_rate}Hz

    Just play! Press <esc> to exit...
    """)
  
  def update(self, osc, time_axis, sample, xlimits): pass