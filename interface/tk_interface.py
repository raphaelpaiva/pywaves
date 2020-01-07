import tkinter
import logging

from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import LabelFrame
from tkinter.ttk import Scale

from .widgets import (Knob, SynthFrame, KnobFrame, VisualizationFrame, OscilatorFrame)

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

    self.plot_frames = []
    self.update_frames = []

    self._create_window()

  def _create_window(self):
    self.master.title("JustASynth")

    self._create_oscilator_section().pack(side=tkinter.LEFT)
    self._create_master().pack(side=tkinter.LEFT)

    self.pack()

  def _create_master(self):
    output_device = self.player.get_output_device()
    
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
      text=f"Device: {output_device['name']}"
    ).pack()

    Label(
      master_frame,
      text=f"Channels: {self.player.channels}"
    ).pack()

    Label(
      master_frame,
      text=f"Sample Rate: {output_device['default_samplerate']}Hz"
    ).pack()

    Label(
      master_frame,
      text=f"Block Size: {self.player.stream.blocksize}"
    ).pack()

    Label(
      master_frame,
      text=f"Latency: {self.player.stream.latency * 1000}ms"
    ).pack()

    graph_frame = self._create_graph_frame(master_frame, lambda: self.player.master_sample)
    graph_frame.pack()
    
    self.plot_frames.append(graph_frame)

    return master_frame

  def _create_oscilator_section(self):
    osc_section = SynthFrame(self, "Oscilators")

    for osc in self.oscilators:
      osc_frame = self._create_oscilator(osc_section, osc)
      osc_frame.pack()
      self.update_frames.append(osc_frame)

    return osc_section

  def _create_oscilator(self, master, oscilator):
    osc_frame = OscilatorFrame(
      master,
      oscilator,
      self.sampler.sample_size / self.sampler.sample_rate,
      self.sampler.sample_rate
    )

    return osc_frame

  def _create_graph_frame(self, master, data_source):
    graph_frame = VisualizationFrame(
      master,
      data_source
    )

    return graph_frame

  def update_canvas(self):
    for frame in self.plot_frames:
      frame.plot()
    
    for frame in self.plot_frames + self.update_frames:
      frame.update_canvas()

    self.after(0, self.update_canvas)

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

  def update(self, osc, time_axis, sample, xlimits): pass
