import threading
import tkinter

from tkinter import Frame
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Scale
from tkinter import Button

from sinusoud import Sinusoid
from oscilator import Oscilator
from player import Player

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master, padx=10, pady=5)
    self.master = master
    self.stop   = False
    
    self.oscilator     = Oscilator()
    self.player        = Player()
    self.player_thread = threading.Thread(target=self._continuous_play)
    
    self._create_window()
    
    self.player_thread.start()

  def _create_window(self):
    self.master.title("JustASynth")
    
    osc_frame = self._create_osc(self.oscilator)
    osc_frame.grid()

    self.grid()
  
  def _create_osc(self, osc):
    osc_frame = LabelFrame(
      self,
      text=osc.name,
      relief=tkinter.GROOVE,
      borderwidth=5
    )

    
    freq_tracker = tkinter.IntVar()
    freq_tracker.set(osc.wave.frequency)

    Scale(
      osc_frame,
      variable=freq_tracker,
      label="Frequency",
      from_=20,
      to=5000,
      orient=tkinter.HORIZONTAL,
      command=osc.set_frequency,
      length=400
    ).grid(row=0, column=0)

    vol_tracker = tkinter.DoubleVar()
    vol_tracker.set(self.player.volume)

    Scale(
      osc_frame,
      variable=vol_tracker,
      label="Volume",
      from_=0.0,
      to=1.0,
      orient=tkinter.HORIZONTAL,
      command=osc.set_volume,
      resolution=0.01
    ).grid(row=1, column=0, sticky=tkinter.W)

    return osc_frame

  
  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration
      
      sample, _ = self.oscilator.wave.sample(duration, sample_rate, start_time=time)

      self.player.play_sample(sample)

      t += 1

  def terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()


def main():
  root = tkinter.Tk()

  root.geometry("")

  app = Window(root)
  
  root.mainloop()

  app.terminate()

if __name__ == "__main__":
  main()

