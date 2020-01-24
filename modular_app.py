import time

from synth.modular_synth import ModularSynth, Command

def detune(s):
  for i in range(30000):
    val = (i/30000.0)
    s.input(Command('set', 'Saw', 'volume', val))

s = ModularSynth()
s.start()
s.input(Command('add', 'Sine'))
s.input(Command('set', 'Sine', 'volume', 0.2))
s.input(Command('add', 'Saw'))
s.input(Command('set', 'Saw', 'waveform', 2))
s.input(Command('play', 220))
s.input(Command('play', 110))

detune(s)

s.process()
time.sleep(2)

s.stop()