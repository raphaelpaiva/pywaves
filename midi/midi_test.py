import unittest

from midi import note_to_midi_number, midi_number_to_freq, note_on, note_off
from midi import MidiException

# note, octave, midi_number, freq
note_to_midi_number_tests = [
  ("C", -1, 0, 8.1),
  ("C#", -1, 1, 8.6),
  ("D", -1, 2, 9.1),
  ("D#", -1, 3, 9.7),
  ("E", -1, 4, 10.3),
  ("F", -1, 5, 10.9),
  ("F#", -1, 6, 11.5),
  ("G", -1, 7, 12.2),
  ("G#", -1, 8, 12.9),
  ("A", -1, 9, 13.7),
  ("A#", -1, 10, 14.5),
  ("B", -1, 11, 15.4),
  ("C", 0, 12, 16.3),
  ("C#", 0, 13, 17.3),
  ("D", 0, 14, 18.3),
  ("D#", 0, 15, 19.4),
  ("E", 0, 16, 20.6),
  ("F", 0, 17, 21.8),
  ("F#", 0, 18, 23.1),
  ("G", 0, 19, 24.4),
  ("G#", 0, 20, 25.9),
  ("A", 0, 21, 27.5),
  ("A#", 0, 22, 29.1),
  ("B", 0, 23, 30.9),
  ("C", 1, 24, 32.7),
  ("C#", 1, 25, 34.6),
  ("D", 1, 26, 36.7),
  ("D#", 1, 27, 38.9),
  ("E", 1, 28, 41.2),
  ("F", 1, 29, 43.7),
  ("F#", 1, 30, 46.2),
  ("G", 1, 31, 49.0),
  ("G#", 1, 32, 51.9),
  ("A", 1, 33, 55.0),
  ("A#", 1, 34, 58.3),
  ("B", 1, 35, 61.7),
  ("C", 2, 36, 65.4),
  ("C#", 2, 37, 69.3),
  ("D", 2, 38, 73.4),
  ("D#", 2, 39, 77.8),
  ("E", 2, 40, 82.4),
  ("F", 2, 41, 87.3),
  ("F#", 2, 42, 92.5),
  ("G", 2, 43, 98.0),
  ("G#", 2, 44, 103.8),
  ("A", 2, 45, 110.0),
  ("A#", 2, 46, 116.5),
  ("B", 2, 47, 123.5),
  ("C", 3, 48, 130.8),
  ("C#", 3, 49, 138.6),
  ("D", 3, 50, 146.8),
  ("D#", 3, 51, 155.6),
  ("E", 3, 52, 164.8),
  ("F", 3, 53, 174.6),
  ("F#", 3, 54, 185.0),
  ("G", 3, 55, 196.0),
  ("G#", 3, 56, 207.7),
  ("A", 3, 57, 220.0),
  ("A#", 3, 58, 233.1),
  ("B", 3, 59, 246.9),
  ("C", 4, 60, 261.6),
  ("C#", 4, 61, 277.2),
  ("D", 4, 62, 293.7),
  ("D#", 4, 63, 311.1),
  ("E", 4, 64, 329.6),
  ("F", 4, 65, 349.2),
  ("F#", 4, 66, 370.0),
  ("G", 4, 67, 392.0),
  ("G#", 4, 68, 415.3),
  ("A", 4, 69, 440.0),
  ("A#", 4, 70, 466.2),
  ("B", 4, 71, 493.9),
  ("C", 5, 72, 523.3),
  ("C#", 5, 73, 554.4),
  ("D", 5, 74, 587.3),
  ("D#", 5, 75, 622.3),
  ("E", 5, 76, 659.3),
  ("F", 5, 77, 698.5),
  ("F#", 5, 78, 740.0),
  ("G", 5, 79, 784.0),
  ("G#", 5, 80, 830.6),
  ("A", 5, 81, 880.0),
  ("A#", 5, 82, 932.3),
  ("B", 5, 83, 987.8),
  ("C", 6, 84, 1046.5),
  ("C#", 6, 85, 1108.7),
  ("D", 6, 86, 1174.7),
  ("D#", 6, 87, 1244.5),
  ("E", 6, 88, 1318.5),
  ("F", 6, 89, 1396.9),
  ("F#", 6, 90, 1480.0),
  ("G", 6, 91, 1568.0),
  ("G#", 6, 92, 1661.2),
  ("A", 6, 93, 1760.0),
  ("A#", 6, 94, 1864.7),
  ("B", 6, 95, 1975.5),
  ("C", 7, 96, 2093.0),
  ("C#", 7, 97, 2217.5),
  ("D", 7, 98, 2349.3),
  ("D#", 7, 99, 2489.0),
  ("E", 7, 100, 2637.0),
  ("F", 7, 101, 2793.8),
  ("F#", 7, 102, 2960.0),
  ("G", 7, 103, 3136.0),
  ("G#", 7, 104, 3322.4),
  ("A", 7, 105, 3520.0),
  ("A#", 7, 106, 3729.3),
  ("B", 7, 107, 3951.1),
  ("C", 8, 108, 4186.0),
]

class MidiTest(unittest.TestCase):

  def test_midiNoteToNumber_AllNotesAndOctaves(self):
    for test in note_to_midi_number_tests:
      note, octave, expected_value, _ = test
      actual_value = note_to_midi_number(note, octave)

      self.assertEqual(actual_value, expected_value)

  def test_midiNoteToNumber_NonExistingNote(self):
    with self.assertRaises(MidiException) as me:
      note_to_midi_number("x", 0)

    self.assertEqual(me.exception.message, "'x' is not a Midi note.")

  def test_midiNoteToNumber_NoneOctave(self):
    with self.assertRaises(MidiException) as me:
      note_to_midi_number("A", None)

    self.assertEqual(me.exception.message, "Octave value should be integer. Recieved None.")

  def test_note_on_ShouldHaveCorrectStatusCode(self):
    expected_status_code = 0x90

    midi_msg = note_on('A', 2, 128)
    actual_status_code = midi_msg.status

    self.assertEqual(actual_status_code, expected_status_code)

  def test_note_off_ShouldHaveCorrectStatusCode(self):
    expected_status_code = 0x80

    midi_msg = note_off('A', 2, 128)
    actual_status_code = midi_msg.status

    self.assertEqual(actual_status_code, expected_status_code)

  def test_midiNumberTofreq(self):
    for test in note_to_midi_number_tests:
      _, _, note_number, expected_freq = test
      actual_value = midi_number_to_freq(note_number)

      self.assertAlmostEqual(actual_value, expected_freq, delta=0.1)