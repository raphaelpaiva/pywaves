import tkinter
import logging
import math
import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale
from tkinter.ttk import Button
from tkinter import TclError

from .widgets import (Knob, SynthFrame, KnobFrame)

LOGGER_NAME = 'TkInterface'

class Window(Frame):
  def __init__(self, synth, log, master=None):
    Frame.__init__(
      self,
      master
    )
    
    self.master = master
    self.log = log
    
    self.synth = synth
    self.player = synth.player
    self.sampler = synth.sampler
    self.oscilators = synth.oscilators

    self.lines = {}
    self.canvas = {}
    self.axes = {}

    for osc in self.oscilators:
      self.lines[osc] = None
      self.canvas[osc] = None
      self.axes[osc] = None

    self.lines["master"] = None
    self.canvas["master"] = None
    self.axes["master"] = None

    self._create_window()

  def _create_window(self):
    self.master.title("JustASynth")

    self._create_oscilator_section().pack(side=tkinter.LEFT)
    self._create_master().pack(side=tkinter.LEFT)

    self.pack()

  def _create_master(self):
    master_frame = LabelFrame(
      self,
      text="Master",
      relief=tkinter.GROOVE,
      borderwidth=5
    )

    Label(
      master_frame,
      text="Volume"
    ).pack()

    vol_tracker = tkinter.DoubleVar()
    vol_tracker.set(self.player.volume)

    Scale(
      master_frame,
      variable=vol_tracker,
      from_=1.0,
      to=0.0,
      orient=tkinter.VERTICAL,
      command=self.player.set_volume,
    ).pack()

    Label(
      master_frame,
      text=f"Channels: {self.player.channels}"
    ).pack()

    Label(
      master_frame,
      text=f"Sample Size: {self.player.sample_size}"
    ).pack()

    Label(
      master_frame,
      text=f"Sample Rate: {self.player.sample_rate}Hz"
    ).pack()

    self._create_graph_frame("master", master_frame, ylim=(-1,1)).pack()

    return master_frame

  def _create_oscilator_section(self):
    osc_section = SynthFrame(self, "Oscilators")

    for osc in self.oscilators:
      self._create_oscilator(osc_section, osc).pack()

    return osc_section

  def _create_oscilator(self, master, oscilator):
    osc_frame = SynthFrame(
      master,
      text=oscilator.name
    )

    self._create_graph_frame(oscilator, osc_frame).pack(side=tkinter.LEFT)
    
    KnobFrame(
      osc_frame,
      "Phase",
      command=oscilator.set_phase,
      max_value=2 * math.pi,
      label_format=lambda x: f"{(x/math.pi):.2f}π"
    ).pack(side=tkinter.LEFT)
    
    KnobFrame(
      osc_frame,
      "Volume",
      command=oscilator.set_volume,
      label_format="{:.2f}"
    ).pack(side=tkinter.LEFT)

    return osc_frame

  def _create_graph_frame(self, osc, master_widget, ylim=(-1,1)):
    graph_frame = LabelFrame(
        master_widget,
        text="Graph",
        relief=tkinter.GROOVE,
        borderwidth=5
      )

    fig = Figure((2,1))

    ax = fig.add_subplot(111)
    self.axes[osc] = ax

    line, = ax.plot(0)

    ax.set_xlim((0, 1/self.player.sample_rate))
    ax.set_ylim(ylim)
    ax.set_xticks([])
    ax.set_yticks([])

    self.lines[osc] = line

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    self.canvas[osc] = canvas

    return graph_frame

  def update_canvas(self):
    master_data = self.player.master_sample

    if master_data is not None:
      self.update_osc_data('master', np.arange(len(master_data)), master_data)
    
    for canvas in self.canvas.values():
      try:
        canvas.draw()
        canvas.flush_events()
      except TclError:
        break

    self.after(0, self.update_canvas)

  def update_osc_data(self, osc, time_axis, sample, xlimits=None):
    if xlimits is None:
      xlimits = (0, len(sample))
    
    self.lines[osc].set_data(time_axis, sample)
    self.axes[osc].set_xlim(xlimits)

class TkInterface(object):
  def __init__(self, synth, log=None):
    self.log = log.getChild(LOGGER_NAME) if log else logging.getLogger(LOGGER_NAME)
    self.root = tkinter.Tk()
    self.root.geometry("")
    
    self.window = Window(synth, self.log, self.root)
    self.window.after(0, self.window.update_canvas)
  
  def start(self, exit_action=None):
    if exit_action:
      self.root.protocol("WM_DELETE_WINDOW", exit_action)
    
    self.root.mainloop()

  def stop(self):
    self.window.destroy()
    self.root.destroy()

  def update(self, osc, time_axis, sample, xlimits):
    self.window.update_osc_data(osc, time_axis, sample, xlimits)
