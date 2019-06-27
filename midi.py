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

midi_status = {
  "note_off": 0x80,
  "note_on":  0x90,
}

def note_to_midi_number(note, octave):
  return midi_note_table[note] + 12*(octave + 2)

# TODO: Test this
def midi_number_to_freq(note_number):
 pitch = (note_number - 69) / 12
 freq = 440 * 2 ** pitch

 return freq

def note_on(note, octave, velocity):
  note_number = note_to_midi_number(note, octave)
  status = midi_status['note_on']

  return MidiMessage(
    status,
    note_number,
    velocity
  )

def note_off(note, octave, velocity):
  note_number = note_to_midi_number(note, octave)
  status = midi_status['note_off']
  
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