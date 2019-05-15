#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy

pi = numpy.pi
sin = numpy.sin

f = 440 # Hz
w = 2 * pi * f
t = numpy.arange(0.0, 100, 0.0001)
phase = 2

fig = plt.figure()

def generate_static_data():
  baseline_data = [sin(w * i) for i in t]
  mod_data = [sin(w * i + phase) for i in t]
  result_data = [x + y for x,y in zip(baseline_data, mod_data)]

  return baseline_data, mod_data, result_data

def plot(x_data, baseline_data, mod_data, result_data):
  base_graph = fig.add_subplot(211)

  baseline = base_graph.plot(x_data, baseline_data)
  gainline = base_graph.plot(x_data, mod_data)

  result_graph = fig.add_subplot(212, sharex=base_graph)
  resultline = result_graph.plot(x_data, result_data)

  plt.setp(gainline, color='g')
  plt.setp(resultline, color='r')
  plt.ylim(-1.5, 1.5)
  plt.xlim(0.0, 0.01)

  return baseline, gainline, resultline

def update(tick, baseline, modline, resultline):
  rad = w * tick

  base = sin(rad)
  mod = sin(rad + phase)
  result = base + mod

  xdata, baseydata = baseline.get_data()
  modydata = modline.get_ydata()
  resultydata = resultline.get_ydata()

  xdata.append(tick)
  baseydata.append(base)
  modydata.append(mod)
  resultydata.append(result)

  baseline.set_data(xdata, baseydata)
  modline.set_data(xdata, modydata)
  resultline.set_data(xdata, resultydata)

def main():
  plt.ion()
  plt.show()
  
  #baseline_data, mod_data, result_data = generate_static_data()

  baseline, modline, resultline = plot([], [], [], [])

  update(0.5, baseline, modline, resultline)
  plt.draw()


if __name__ == "__main__":
    main()
