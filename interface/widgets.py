import tkinter as tk
from tkinter import ttk

import math

import numpy as np

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

class Knob(tk.Frame):
  def __init__(self, parent, radius=25, lock=False, max_angle=360, min_angle=0, init_angle=None, step_ratio=1, command=None, **kwargs):
    size_adjust = 2
    diameter = 2 * radius
    size = diameter + size_adjust

    super().__init__(parent)

    self.line = None
    self.min_angle = min_angle
    self.max_angle = max_angle
    self.step_ratio = step_ratio
    self.command = command
    
    self.center = (self.winfo_rootx() + radius + size_adjust, self.winfo_rooty() + radius + size_adjust)
    self.radius = radius
    self.angular_amplitude = max_angle - min_angle
    
    self.canvas = tk.Canvas(self, width=size, height=size)
    self.canvas.pack()
    
    self.angle = init_angle if init_angle is not None else (self.min_angle + self.max_angle) / 2
    self._update_value(self.angle)

    if max_angle < 360 or self.min_angle > 0:
      self.lock=True
    else:
      self.lock = lock

    self._draw_circle(**kwargs)
    self._draw_line(**kwargs)

    self.last_mouse_y = None
    self.canvas.bind("<B1-Motion>", self._update_angle)
    self.canvas.bind("<ButtonRelease-1>", self._release)

  def _draw_circle(self, **kwargs):
    cx, cy = self.center
    r = self.radius

    self.circle = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r)

  def _calculate_line_coordinates(self):
    cx, cy = self.center
    r = self.radius
    rads = math.radians(self.angle)

    x0, y0 = self.center
    x1 = cx + r * math.cos(rads)
    y1 = cy - r * math.sin(rads)

    return x0, y0, x1, y1

  def _draw_line(self, **kwargs):
    if self.line is None:
      self.line = self.canvas.create_line(*self._calculate_line_coordinates())
    else:
      self.canvas.coords(self.line, *self._calculate_line_coordinates())

  def _update_angle(self, event):
    if self.last_mouse_y is not None:
      dy = event.y - self.last_mouse_y

      new_angle = self.angle + dy * self.step_ratio

      self.set_angle(new_angle)
      self._update_value(new_angle)

    self.last_mouse_y = event.y
    self._draw_line()

  def _update_value(self, new_angle):
    angular_step  = new_angle - self.min_angle            # how far away is the new angle from the minimum?
    angular_ratio = angular_step / self.angular_amplitude # how much of the total is this step?
    new_value = angular_ratio                             # The value must vary at the same rate as the angle  
    
    if new_value < 0:
      new_value = 0
    if new_value > 1.0:
      new_value = 1

    self.value = new_value
    
    if self.command:
      self.command(self.value)

  def _release(self, event):
    self.last_mouse_y = None

  def set_angle(self, angle):
    self.angle = max(self.min_angle, min(angle, self.max_angle)) if self.lock else angle % (abs(self.max_angle) - abs(self.min_angle))

class SynthFrame(ttk.LabelFrame):
  """ Just a ttk.LabelFrame with Groove relief and 5px borderwidth"""
  def __init__(self, master, text):
    super().__init__(
      master,
      text=text,
      relief=tk.GROOVE,
      borderwidth=5
    )

class KnobFrame(SynthFrame):
  def __init__(self, master, name="Knob", command=None, max_value=1.0, label_format=None, invert_value=True):
    super().__init__(
      master,
      name
    )

    self.command = command
    self.max_value = max_value
    self.label_format = label_format
    self.invert_value = invert_value
    
    self.text_var = tk.StringVar()

    Knob(
      self,
      15,
      min_angle=-45,
      max_angle=225,
      command=self._update_value
    ).pack()
    
    ttk.Label(self, textvariable=self.text_var, borderwidth=1, relief="solid").pack()

  def _update_value(self, knob_value):
    if self.invert_value:
      value = (1.0 - knob_value) * self.max_value
    else:
      value = knob_value * self.max_value
    
    self.command(value)
    
    lbl_val = value
    
    if self.label_format is not None:
      if callable(self.label_format):
        lbl_val = self.label_format(value)
      elif isinstance(self.label_format, str):
        lbl_val = self.label_format.format(value)

    self.text_var.set(lbl_val)

class VisualizationFrame(SynthFrame):
  def __init__(self, master, data, name="Visualization"):
    super().__init__(master, name)
    self.data = data
    self._init_plot_components()
  
  def _init_plot_components(self):
    fig = Figure((2,1))

    self.ax = fig.add_subplot(111)
    self.line, = self.ax.plot(0)
    self.canvas = FigureCanvasTkAgg(fig, master=self)

    self.ax.set_xlim((0, 1))
    self.ax.set_ylim((-1,1))
    self.ax.set_xticks([])
    self.ax.set_yticks([])
    
    self.canvas.get_tk_widget().pack()

  def plot(self):
    data = self.data() if callable(self.data) else self.data
    
    data_size = len(data)
    time_axis = np.arange(data_size)
    xlimits = (0, data_size)

    self.line.set_data(time_axis, data)
    self.ax.set_xlim(xlimits)

  def update_canvas(self):
    try:
      self.canvas.draw()
      self.canvas.flush_events()
    except tk.TclError:
      pass

class OscilatorFrame(SynthFrame):
  def __init__(self, master, oscilator, vizualization_duration, vizualization_sample_rate):
    super().__init__(master, oscilator.name)
    self.oscilator = oscilator
    
    data_source = lambda: oscilator.wave.sample(vizualization_duration, vizualization_sample_rate)
    self.graph_frame = VisualizationFrame(self, data_source)
    self.graph_frame.pack(side=tk.LEFT)
    
    KnobFrame(
      self,
      "Phase",
      command=self.update_phase,
      max_value=2 * math.pi,
      label_format=lambda x: f"{(x/math.pi):.2f}π"
    ).pack(side=tk.LEFT)
    
    KnobFrame(
      self,
      "Volume",
      command=self.update_volume,
      label_format="{:.2f}"
    ).pack(side=tk.LEFT)
  
  def update_phase(self, value):
    self.oscilator.set_phase(value)
    self.graph_frame.plot()
  
  def update_volume(self, value):
    self.oscilator.set_volume(value)
    self.graph_frame.plot()
  
  def update_canvas(self):
    self.graph_frame.update_canvas()