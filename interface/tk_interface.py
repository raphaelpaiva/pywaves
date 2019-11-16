import tkinter
import logging
import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale
from tkinter.ttk import Button
from tkinter import TclError

from .rotary import Knob

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

    osc_frames = self._create_osc()
    for frame in osc_frames:
      frame.grid()

    master_frame = self._create_master()
    master_frame.grid(row=0, column=1)

    self.grid()

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
    ).grid()

    vol_tracker = tkinter.DoubleVar()
    vol_tracker.set(self.player.volume)

    Scale(
      master_frame,
      variable=vol_tracker,
      from_=1.0,
      to=0.0,
      orient=tkinter.VERTICAL,
      command=self.player.set_volume,
    ).grid()

    Label(
      master_frame,
      text=f"Channels: {self.player.channels}"
    ).grid(sticky=tkinter.W)

    Label(
      master_frame,
      text=f"Sample Size: {self.player.sample_size}"
    ).grid(sticky=tkinter.W)

    Label(
      master_frame,
      text=f"Sample Rate: {self.player.sample_rate}Hz"
    ).grid(sticky=tkinter.W)

    self._create_graph_frame("master", master_frame, ylim=(-1,1)).grid()

    return master_frame

  def _create_osc(self):
    osc_frames = []

    for osc in self.oscilators:
      osc_frame = LabelFrame(
        self,
        text=osc.name,
        relief=tkinter.GROOVE,
        borderwidth=5
      )

      phase_frame = LabelFrame(
        osc_frame,
        text="Phase",
        relief=tkinter.GROOVE,
        borderwidth=5
      )

      Knob(
        phase_frame,
        15,
        width=2,
        min_angle=-45,
        max_angle=225,
        max_value=12.566370614359172953850573533118,
        min_value=0,
        command=osc.set_phase
      ).grid(row=3, column=1, sticky=tkinter.W)
      
      phase_frame.grid(row=0, column=1, sticky=tkinter.W)

      volume_frame = LabelFrame(
        osc_frame,
        text="Volume",
        relief=tkinter.GROOVE,
        borderwidth=5
      )

      Knob(
        volume_frame,
        15,
        width=2,
        min_angle=-45,
        max_angle=225,
        max_value=1.0,
        min_value=0.0,
        command=osc.set_volume
      ).grid(row=5, column=2, sticky=tkinter.W)

      volume_frame.grid(row=0, column=2, sticky=tkinter.W)

      graph_frame = self._create_graph_frame(osc, osc_frame)

      graph_frame.grid(row=0, column=0)

      osc_frames.append(osc_frame)

    return osc_frames

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
    canvas.get_tk_widget().grid()

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
