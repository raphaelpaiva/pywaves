import tkinter
import logging

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale

class DebugWindow(Frame):
  def __init__(self, master=None, synth=None):
    if not synth:
      raise Exception("No synth, no debug!")
    super().__init__(master)
    Label(self, text="Opa!").pack()
    self.pack()