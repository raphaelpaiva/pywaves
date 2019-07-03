midi_note_table = {
  "C":  0,
  "C#": 1,
  "D":  2,
  "D#": 3,
  "E":  4,
  "F":  5,
  "F#": 6,
  "G":  7,
  "G#": 8,
  "A":  9,
  "A#": 10,
  "B":  11
}

ST_NOTE_OFF = 0x80
ST_NOTE_ON  = 0x90

EVT_MIDI    = 'midi_'

def note_to_midi_number(note, octave):
  if note not in midi_note_table:
    raise MidiException(f"'{note}' is not a Midi note.")
  if not isinstance(octave, int):
    raise MidiException(f"Octave value should be integer. Recieved {octave}.")

  base_note = midi_note_table[note]
  return base_note + 12*(octave + 1)

# TODO: Test this
def midi_number_to_freq(note_number):
 pitch = (note_number - 69) / 12
 freq = 440 * 2 ** pitch

 return freq

def note_on(note, octave, velocity):
  note_number = note_to_midi_number(note, octave)
  status = ST_NOTE_ON

  return MidiMessage(
    status,
    note_number,
    velocity
  )

def note_off(note, octave, velocity):
  note_number = note_to_midi_number(note, octave)
  status = ST_NOTE_OFF

  return MidiMessage(
    status,
    note_number,
    velocity
  )

class MidiMessage(object):
  def __init__(self, status, data1, data2):
    self.status = status
    self.data1  = data1
    self.data2  = data2

  def __str__(self):
    return f"MidiMessage({self.status:x}; {self.data1:x}; {self.data2:x})"

class MidiException(Exception):
  def __init__(self, message):
    super().__init__(self, message)

    self.message = message
