import tkinter
import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale
from tkinter.ttk import Button
from tkinter import TclError

from sinusoud import Sinusoid, Triangle
from oscilator import Oscilator
from player import Player

class Window(Frame):
  def __init__(self, synth, master=None):
    Frame.__init__(
      self,
      master
    )
    
    self.master = master
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
    #for frame in osc_frames:
    #  frame.grid()

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

    self._create_graph_frame("master", master_frame, ylim=(1,-1)).grid()

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

      freq_tracker = tkinter.DoubleVar()
      freq_tracker.set(float(osc.wave.frequency))

      Label(
        osc_frame,
        text="Frequency"
      ).grid(row=1, column=0)

      Label(
        osc_frame,
        textvariable=freq_tracker
      ).grid(row=0, column=1)

      Scale(
        osc_frame,
        variable=freq_tracker,
        from_=20,
        to=5000,
        orient=tkinter.HORIZONTAL,
        command=osc.set_frequency,
        length=400
      ).grid(row=1, column=1)

      phase_tracker = tkinter.DoubleVar()
      phase_tracker.set(float(osc.wave.phase))

      Label(
        osc_frame,
        text="Phase"
      ).grid(row=3, column=0, sticky=tkinter.W)

      Label(
        osc_frame,
        textvariable=phase_tracker
      ).grid(row=2, column=1)

      Scale(
        osc_frame,
        variable=phase_tracker,
        from_=0,
        to=12.566370614359172953850573533118, # 4 * PI Lazy
        orient=tkinter.HORIZONTAL,
        command=osc.set_phase,
        length=100
      ).grid(row=3, column=1, sticky=tkinter.W)

      vol_tracker = tkinter.DoubleVar()
      vol_tracker.set(float(osc.volume))

      Label(
        osc_frame,
        text="Volume"
      ).grid(row=5, column=0, sticky=tkinter.W)

      Label(
        osc_frame,
        textvariable=vol_tracker
      ).grid(row=4, column=1)

      Scale(
        osc_frame,
        variable=vol_tracker,
        from_=0.0,
        to=1.0,
        orient=tkinter.HORIZONTAL,
        command=osc.set_volume,
      ).grid(row=5, column=1, sticky=tkinter.W)

      graph_frame = self._create_graph_frame(osc, osc_frame)

      graph_frame.grid(row=6, column=0)

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
  def __init__(self, synth):
    self.root = tkinter.Tk()
    self.root.geometry("")
    
    self.window = Window(synth, self.root)
    self.window.after(0, self.window.update_canvas)
  
  def start(self):
    self.root.mainloop()

  def update(self, osc, time_axis, sample, xlimits):
    self.window.update_osc_data(osc, time_axis, sample, xlimits)

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