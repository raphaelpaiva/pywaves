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
    self.sinusoid = Sinusoid()
    self.player = Player()
    
    self._create_window()

  def _create_window(self):
    self.master.title("JustASynth")
    frequencyTracker = tkinter.IntVar()
    frequencyTracker.set(self.sinusoid.frequency)

    scale = Scale(
      self,
      variable=frequencyTracker,
      label="Frequency",
      from_=100,
      to=880,
      orient=tkinter.HORIZONTAL,
      command=self._setFrequency
    )
    
    scale.grid(row=0, column=0)

    button = Button(self, text="Sample", command=self._sample)
    button.grid(row=0, column=1)

    self.grid()

  def _sample(self):
    self.player.play_sample(self.sinusoid.sample(2, self.player.sample_rate))
  
  def _setFrequency(self, freq):
    self.sinusoid.frequency = int(freq)

  def terminate(self):
    self.player.terminate()


def main():
  root = tkinter.Tk()

  root.geometry("400x300")

  app = Window(root)
  
  root.mainloop()

  app.terminate()

if __name__ == "__main__":
  main()

