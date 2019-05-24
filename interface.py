import threading
import tkinter

from tkinter import Frame
from tkinter import Label
from tkinter import Scale
from tkinter import Button

from sinusoud import Sinusoid
from player import Player

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master
    self.stop = False
    
    self.sinusoid = Sinusoid()
    self.player = Player()
    self.player_thread = threading.Thread(target=self._continuous_play)
    
    self._create_window()
    
    self.player_thread.start()

  def _create_window(self):
    self.master.title("JustASynth")
    
    frequencyTracker = tkinter.IntVar()
    frequencyTracker.set(self.sinusoid.frequency)

    freq_scale = Scale(
      self,
      variable=frequencyTracker,
      label="Frequency",
      from_=20,
      to=5000,
      orient=tkinter.HORIZONTAL,
      command=self._setFrequency,
      length=400
    )
    
    freq_scale.grid(row=0, column=0)

    volTracker = tkinter.DoubleVar()
    volTracker.set(self.player.volume)

    vol_scale = Scale(
      self,
      variable=volTracker,
      label="Volume",
      from_=1.0,
      to=0.0,
      command=self._setVolume,
      resolution=0.01
    )
    
    vol_scale.grid(row=1, column=1)

    self.pack()
  
  def _setFrequency(self, freq):
    self.sinusoid.frequency = int(freq)

  def _setVolume(self, volume):
    self.player.volume = float(volume)
  
  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration = sample_size / sample_rate
      
      sample, _ = self.sinusoid.sample(duration, sample_rate, start_time=t * duration)

      self.player.play_sample(sample)

      t += 1

  def terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()


def main():
  root = tkinter.Tk()

  root.geometry("600x300")

  app = Window(root)
  
  root.mainloop()

  app.terminate()

if __name__ == "__main__":
  main()

