import tkinter as tk
import math

class Knob(tk.Frame):
  def __init__(self, parent, radius, lock=False, max_angle=365, min_angle=0, **kwargs):
    size_adjust = 2
    diameter = 2 * radius
    size = diameter + size_adjust

    super().__init__(parent)

    self.center = (self.winfo_rootx() + radius + size_adjust, self.winfo_rooty() + radius + size_adjust)
    self.radius = radius
    self.angle = 180 + 45
    self.line = None
    self.min_angle = min_angle
    self.max_angle = max_angle

    if max_angle < 365 or self.min_angle > 0:
      self.lock=True
    else:
      self.lock = lock

    self.canvas = tk.Canvas(self, width=size, height=size)
    self.canvas.pack()

    self.text = tk.StringVar(value=self.angle)
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

      self.set_angle(self.angle + dy)

    self.last_mouse_y = event.y

  def _release(self, event):
    self.last_mouse_y = None

  def set_angle(self, angle):
    self.angle = max(self.min_angle, min(angle, self.max_angle)) if self.lock else angle % 365
    self._draw_line()
    self.text.set(self.angle)

def main():
  root = tk.Tk()
  root.geometry("")

  r = 25

  k1 = Knob(root, r, width=2)
  k1.pack()

  k2 = Knob(root, r, width=2, lock=True)
  k2.pack()

  root.mainloop()

if __name__ == "__main__":
  main()
