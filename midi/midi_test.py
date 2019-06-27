import unittest

from midi import note_to_midi_number, note_on, note_off
from midi import MidiException

# note, octave, expected
note_to_midi_number_tests = [
  ("C", -2, 0),
  ("C#", -2, 1),
  ("D", -2, 2),
  ("D#", -2, 3),
  ("E", -2, 4),
  ("F", -2, 5),
  ("F#", -2, 6),
  ("G", -2, 7),
  ("G#", -2, 8),
  ("A", -2, 9),
  ("A#", -2, 10),
  ("B", -2, 11),
  ("C", -1, 12),
  ("C#", -1, 13),
  ("D", -1, 14),
  ("D#", -1, 15),
  ("E", -1, 16),
  ("F", -1, 17),
  ("F#", -1, 18),
  ("G", -1, 19),
  ("G#", -1, 20),
  ("A", -1, 21),
  ("A#", -1, 22),
  ("B", -1, 23),
  ("C", 0, 24),
  ("C#", 0, 25),
  ("D", 0, 26),
  ("D#", 0, 27),
  ("E", 0, 28),
  ("F", 0, 29),
  ("F#", 0, 30),
  ("G", 0, 31),
  ("G#", 0, 32),
  ("A", 0, 33),
  ("A#", 0, 34),
  ("B", 0, 35),
  ("C", 1, 36),
  ("C#", 1, 37),
  ("D", 1, 38),
  ("D#", 1, 39),
  ("E", 1, 40),
  ("F", 1, 41),
  ("F#", 1, 42),
  ("G", 1, 43),
  ("G#", 1, 44),
  ("A", 1, 45),
  ("A#", 1, 46),
  ("B", 1, 47),
  ("C", 2, 48),
  ("C#", 2, 49),
  ("D", 2, 50),
  ("D#", 2, 51),
  ("E", 2, 52),
  ("F", 2, 53),
  ("F#", 2, 54),
  ("G", 2, 55),
  ("G#", 2, 56),
  ("A", 2, 57),
  ("A#", 2, 58),
  ("B", 2, 59),
  ("C", 3, 60),
  ("C#", 3, 61),
  ("D", 3, 62),
  ("D#", 3, 63),
  ("E", 3, 64),
  ("F", 3, 65),
  ("F#", 3, 66),
  ("G", 3, 67),
  ("G#", 3, 68),
  ("A", 3, 69),
  ("A#", 3, 70),
  ("B", 3, 71),
  ("C", 4, 72),
  ("C#", 4, 73),
  ("D", 4, 74),
  ("D#", 4, 75),
  ("E", 4, 76),
  ("F", 4, 77),
  ("F#", 4, 78),
  ("G", 4, 79),
  ("G#", 4, 80),
  ("A", 4, 81),
  ("A#", 4, 82),
  ("B", 4, 83),
  ("C", 5, 84),
  ("C#", 5, 85),
  ("D", 5, 86),
  ("D#", 5, 87),
  ("E", 5, 88),
  ("F", 5, 89),
  ("F#", 5, 90),
  ("G", 5, 91),
  ("G#", 5, 92),
  ("A", 5, 93),
  ("A#", 5, 94),
  ("B", 5, 95),
  ("C", 6, 96),
  ("C#", 6, 97),
  ("D", 6, 98),
  ("D#", 6, 99),
  ("E", 6, 100),
  ("F", 6, 101),
  ("F#", 6, 102),
  ("G", 6, 103),
  ("G#", 6, 104),
  ("A", 6, 105),
  ("A#", 6, 106),
  ("B", 6, 107),
  ("C", 7, 108),
  ("C#", 7, 109),
  ("D", 7, 110),
  ("D#", 7, 111),
  ("E", 7, 112),
  ("F", 7, 113),
  ("F#", 7, 114),
  ("G", 7, 115),
  ("G#", 7, 116),
  ("A", 7, 117),
  ("A#", 7, 118),
  ("B", 7, 119),
  ("C", 8, 120),
  ("C#", 8, 121),
  ("D", 8, 122),
  ("D#", 8, 123),
  ("E", 8, 124),
  ("F", 8, 125),
  ("F#", 8, 126),
  ("G", 8, 127),
]

class MidiTest(unittest.TestCase):

  def test_midiNoteToNumber_AllNotesAndOctaves(self):
    for test in note_to_midi_number_tests:
      note, octave, expected_value = test
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

