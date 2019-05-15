#!/usr/bin/python

from sinusoud import Sinusoid
import matplotlib.pyplot as plt

wave_sample = Sinusoid(440).sample(1, 44100)

plt.plot(wave_sample)
plt.show()
