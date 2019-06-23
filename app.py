import threading

from interface import TkInterface

from sinusoud import (Sinusoid, Triangle)
from oscilator import Oscilator
from player import Player

class App(object):
  def __init__(self):
    self._init_config()
    self._init_sound_engine()
    self._init_interface()

    self._terminate()
  
  def _init_config(self):
    self.interface = None
    
    self.oscilators = [
      Oscilator(name="Sine", wave=Sinusoid(frequency=303.04429)),
      Oscilator(name="Triangle", wave=Triangle(frequency=303.18527, width=0.5)),
      Oscilator(name="Sawtooth", wave=Triangle(frequency=303.03481, width=0))
    ]
  
  def _init_sound_engine(self):
    self.player        = Player()
    self.player_thread = threading.Thread(target=self._continuous_play)
    
    self.stop = False
    self.player_thread.start()
  
  def _init_interface(self):
    self.interface = TkInterface(self.oscilators, self.player)
    self.interface.start()

  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration

      samples = []

      for osc in self.oscilators:
        sample, time_axis = osc.wave.sample(duration, sample_rate, start_time=time)
        samples.append(sample)
        limits = (time, time + duration)
        self._update_ui(osc, time_axis, sample, limits)

      master, master_time = self.player.mix(samples)
      master_limits = (0, len(master_time))
      
      self._update_ui("master", master_time, master, master_limits)

      self.player.play_sample(master)

      t += 1

  def _update_ui(self, osc, time_axis, sample, limits):
    if self.interface is not None:
      self.interface.update(osc, time_axis, sample, limits)

  def _terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()

def main():
  print("JustASynth")
  App()

if __name__ == "__main__":
    main()
