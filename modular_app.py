import time

from synth.modular_synth import ModularSynth

s = ModularSynth()
s.start()

time.sleep(3)

s.stop()