import threading
from queue import Queue
import input
from input import (KeyboardInput, EVT_KEY, EVT_KEY_PRESSED, EVT_KEY_RELEASED)
import midi
import time

from interface import (TkInterface, CLInterface)

from sinusoud import (Sinusoid, Triangle)
from oscilator import Oscilator
from player import Player

keyboard_note_table = {
  "q": ("E",  4),
  "w": ("F",  4),
  "3": ("F#", 4),
  "e": ("G",  4),
  "4": ("G#", 4),
  "r": ("A",  4),
  "5": ("A#", 4),
  "t": ("B",  4),
  "y": ("C",  5),
  "7": ("C#", 5),
  "u": ("D",  5),
  "8": ("D#", 5),
  "i": ("E",  5),
  "o": ("F",  5),
  "0": ("F#", 5),
  "p": ("G",  5),
  "-": ("G#", 5),
}

class App(object):
  def __init__(self, interface_type):
    self.interface_type = interface_type
    self.interface = None

    self._init_input()
    self._init_generator()
    self._init_sound_engine()
    self._init_interface()

    self._process_queue()

    self._terminate()

  def _init_input(self):
    self.event_queue = Queue()
    self.input = KeyboardInput(self.event_queue)

    self.input.start()

  def _init_generator(self):
    self.oscilators = [
      Oscilator(name="Sine", wave=Sinusoid(frequency=303.04429)),
      Oscilator(name="Triangle", wave=Triangle(frequency=303.18527, width=0.5)),
      Oscilator(name="Sawtooth", wave=Triangle(frequency=303.03481, width=0))
    ]

  def _init_sound_engine(self):
    self.player        = Player()
    self.player_thread = threading.Thread(target=self._continuous_play)

    self.stop = False
    self.player_thread.start()

  def _init_interface(self):
    self.interface = self.interface_type(self.oscilators, self.player)
    self.interface.start()

  def _continuous_play(self):
    t = 0
    while not self.stop:
      sample_size = self.player.sample_size
      sample_rate = self.player.sample_rate
      duration    = sample_size / sample_rate
      time        = t * duration

      samples = []

      for osc in self.oscilators:
        sample, time_axis = osc.wave.sample(duration, sample_rate, start_time=time)
        samples.append(sample)
        limits = (time, time + duration)
        self._update_ui(osc, time_axis, sample, limits)

      master, master_time = self.player.mix(samples)
      master_limits = (0, len(master_time))

      self._update_ui("master", master_time, master, master_limits)

      self.player.play_sample(master)

      t += 1

  def _update_ui(self, osc, time_axis, sample, limits):
    if self.interface is not None:
      self.interface.update(osc, time_axis, sample, limits)

  def _terminate(self):
    self.stop = True
    self.player_thread.join()
    self.player.terminate()

    self.input.stop()

  def _process_queue(self):

    while True:
      event = self.event_queue.get()

      if event is None:
        continue

      event_type, item, e_time = event

      if item == '<esc>':
        break

      if event_type == midi.EVT_MIDI:
        if item.status == midi.ST_NOTE_ON:
          note_number = item.data1
          freq = midi.midi_number_to_freq(note_number)
          for osc in self.oscilators:
            osc.set_frequency(freq)

      if event_type.startswith(EVT_KEY):
        if item not in keyboard_note_table:
          continue

        note, octave = keyboard_note_table[item]
        if event_type == EVT_KEY_PRESSED:
          new_event = (
            midi.EVT_MIDI,
            midi.note_on(note, octave, 127),
            e_time
          )

        if event_type == EVT_KEY_RELEASED:
          new_event = (
            midi.EVT_MIDI,
            midi.note_off(note, octave, 127),
            e_time
          )

        self.event_queue.put(new_event)

def main():
  App(CLInterface)

if __name__ == "__main__":
    main()
