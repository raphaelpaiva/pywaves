#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy

pi = numpy.pi
sin = numpy.sin

f = 440 # Hz
w = 2 * pi * f
t = numpy.arange(0.0, 0.1, 0.0001)
phase = 2

def generate_static_data():
  baseline_data = [sin(w * i) for i in t]
  mod_data = [sin(w * i + phase) for i in t]
  result_data = [x + y for x,y in zip(baseline_data, mod_data)]

  return baseline_data, mod_data, result_data

def plot(baseline_data, mod_data, result_data):
  fig = plt.figure()

  base_graph = fig.add_subplot(211)

  baseline = base_graph.plot(t, baseline_data)
  gainline = base_graph.plot(t, mod_data)

  result_graph = fig.add_subplot(212, sharex=base_graph)
  resultline = result_graph.plot(t, result_data)

  plt.setp(gainline, color='g')
  plt.setp(resultline, color='r')

def main():
  baseline_data, mod_data, result_data = generate_static_data()

  plot(baseline_data, mod_data, result_data)

  plt.show()

if __name__ == "__main__":
    main()
