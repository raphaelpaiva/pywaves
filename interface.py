import tkinter

from tkinter import Frame
from tkinter import Label
from tkinter import Scale
from tkinter import Button

from sinusoud import Sinusoid
from player import play

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master
    self.frequency = 440
    
    self._create_window()


  def _create_window(self):
    self.master.title("JustASynth")
    frequencyTracker = tkinter.IntVar()
    frequencyTracker.set(self.frequency)

    scale = Scale(
      self,
      variable=frequencyTracker,
      label="Frequency",
      from_=100,
      to=880,
      orient=tkinter.HORIZONTAL,
      command=self._setFrequency
    )
    
    scale.grid(row=0, column=1)

    button = Button(self, text="Sample", command=self._sample)
    button.grid(row=0, column=2)

    self.grid()

  def _sample(self):
    play(Sinusoid(frequency=int(self.frequency)))
  
  def _setFrequency(self, freq):
    self.frequency = freq


root = tkinter.Tk()

root.geometry("400x300")

app = Window(root)
root.mainloop()
