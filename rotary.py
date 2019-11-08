import tkinter as tk
import math

class Knob(tk.Frame):
  def __init__(self, parent, radius=25, lock=False, max_angle=360, min_angle=0, init_angle=None, step_ratio=1, min_value=0, max_value=360, show_label=True, label_fmt="{0:.2f}", **kwargs):
    size_adjust = 2
    diameter = 2 * radius
    size = diameter + size_adjust

    super().__init__(parent)

    
    self.line = None
    self.min_angle = min_angle
    self.max_angle = max_angle
    self.step_ratio = step_ratio
    self.min_value = min_value
    self.max_value = max_value
    
    self.center = (self.winfo_rootx() + radius + size_adjust, self.winfo_rooty() + radius + size_adjust)
    self.radius = radius
    self.angular_amplitude = max_angle - min_angle
    self.value_amplitude = max_value - min_value
    
    self.label_fmt = label_fmt
    self.text = tk.StringVar()
    self.canvas = tk.Canvas(self, width=size, height=size)
    
    self.angle = init_angle if init_angle is not None else (self.min_angle + self.max_angle) / 2
    self._update_value(self.angle)

    if max_angle < 360 or self.min_angle > 0:
      self.lock=True
    else:
      self.lock = lock

    
    self.canvas.pack()
    
    if show_label:
      self.label = tk.Label(self, textvariable=self.text, borderwidth=1, relief="solid")
      self.label.pack()

    self._draw_circle(**kwargs)
    self._draw_line(**kwargs)

    self.last_mouse_y = None
    self.canvas.bind("<B1-Motion>", self._update_angle)
    self.canvas.bind("<ButtonRelease-1>", self._release)

  def _draw_circle(self, **kwargs):
    cx, cy = self.center
    r = self.radius

    self.circle = self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, **kwargs)

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
      self.line = self.canvas.create_line(*self._calculate_line_coordinates(), **kwargs)
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
    new_value = self.value_amplitude * angular_ratio      # The value must vary at the same rate as the angle
    
    if new_value > self.max_value:
      new_value = self.max_value
    if new_value < self.min_value:
      new_value = self.min_value
    
    self.value = new_value
    self.text.set(self.label_fmt.format(self.value))

  def _release(self, event):
    self.last_mouse_y = None

  def set_angle(self, angle):
    self.angle = max(self.min_angle, min(angle, self.max_angle)) if self.lock else angle % (abs(self.max_angle) - abs(self.min_angle))

def main():
  root = tk.Tk()
  root.geometry("")

  r = 25

  k1 = Knob(root, 10, width=2, min_angle=-45, max_angle=225, max_value=100, min_value=0)
  k1.pack()

  k2 = Knob(root, r, width=2, min_value=0, max_value=100, lock=True, show_label=False)
  k2.pack()

  root.mainloop()

if __name__ == "__main__":
  main()
