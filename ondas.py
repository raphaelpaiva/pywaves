#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy

pi = numpy.pi
sin = numpy.sin

f = 100 # Hz
w = 2 * pi * f
t = numpy.arange(0.0, 0.1, 0.0001)
phase = 2

def generate_static_data():
  baseline_data = [sin(w * i) for i in t]
  mod_data = [sin(w * i + phase) for i in t]
  result_data = [x + y for x,y in zip(baseline_data, mod_data)]

  return baseline_data, mod_data, result_data

def main():
  baseline_data, mod_data, result_data = generate_static_data()

  plt.subplot(211)
  baseline = plt.plot(t, baseline_data)
  gainline = plt.plot(t, mod_data)

  plt.subplot(212)
  resultline = plt.plot(t, result_data)

  plt.setp(gainline, color='g')
  plt.setp(resultline, color='r', linewidth=2.0)

  plt.ylabel('Sen')
  plt.show()

if __name__ == "__main__":
    main()