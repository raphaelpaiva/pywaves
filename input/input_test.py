from unittest import TestCase, main

from pynput.keyboard import Key, KeyCode
from collections import namedtuple
from queue import Queue
from input.input import KeyboardInput

class KeyboardInputTest(TestCase):
  def _assert_queue_size(self, queue, expected_size=1):
    self.assertFalse(queue.empty(), "Expected the queue not to be empty")
    self.assertEqual(queue.qsize(), expected_size)

  def _assert_midi_message(self, msg, expected_status, expected_note_number):
    self.assertEqual(msg.status, expected_status)
    self.assertEqual(msg.data1, expected_note_number)
    self.assertEqual(msg.data2, 128)

  def test_onpress_SpecialKeyShouldPutKeyInQueue(self):
    queue = Queue()
    key_pressed = Key.esc

    kb = KeyboardInput(queue)
    kb.onpress(key_pressed)

    self._assert_queue_size(queue)

    key = queue.get()

    self.assertIsInstance(key, Key, "Expected queue item to be a pynput.keyboard.Key")
    self.assertEqual(key, Key.esc)

  def test_onpress_OneKeyPressShouldCreateOneMidiOnMessage(self):
    queue = Queue()
    key_pressed = KeyCode.from_char('q')

    kb = KeyboardInput(queue)
    kb.onpress(key_pressed)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_midi_message(msg, 0x90, 64)

  def test_onpress_UnmappedKeyShouldNotPutKeyInQueue(self):
    queue = Queue()
    key_pressed = KeyCode.from_char('b')

    kb = KeyboardInput(queue)
    kb.onpress(key_pressed)

    self.assertTrue(queue.empty(), "Expected the queue to be empty")

  def test_onpress_KeepPressingAKeyShouldPutOnlyOneNoteOnMessageOnTheQueue(self):
    queue = Queue()
    key_pressed = KeyCode.from_char('y')

    kb = KeyboardInput(queue)

    # Holding a key calls onpress multiple times
    kb.onpress(key_pressed)
    kb.onpress(key_pressed)
    kb.onpress(key_pressed)
    kb.onpress(key_pressed)
    kb.onpress(key_pressed)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_midi_message(msg, 0x90, 72)

  def test_onrelease_OneKeyPressShouldCreateOneMidiOnMessage(self):
    queue = Queue()
    key_released = KeyCode.from_char('q')

    kb = KeyboardInput(queue)
    kb.onrelease(key_released)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_midi_message(msg, 0x80, 64)

  def test_onrelease_SpecialKeyShouldNotPutKeyInQueue(self):
    queue = Queue()
    key_released = Key.esc

    kb = KeyboardInput(queue)
    kb.onrelease(key_released)

    self.assertTrue(queue.empty(), "Expected the queue to be empty")

  def test_onrelease_UnmappedKeyShouldNotPutKeyInQueue(self):
    queue = Queue()
    key_released = KeyCode.from_char('b')

    kb = KeyboardInput(queue)
    kb.onrelease(key_released)

    self.assertTrue(queue.empty(), "Expected the queue to be empty")

  # Testing a bug (Issue #1)
  def test_pressReleasePress_shouldNotBlockTheLastPress(self):
    queue = Queue()
    target_key = KeyCode.from_char('y')

    kb = KeyboardInput(queue)

    # Holding a key calls onpress multiple times
    kb.onpress(target_key)
    kb.onrelease(target_key)
    kb.onpress(target_key)

    self._assert_queue_size(queue, 3)

    msg1 = queue.get()
    msg2 = queue.get()
    msg3 = queue.get()

    self._assert_midi_message(msg1, 0x90, 72)
    self._assert_midi_message(msg2, 0x80, 72)
    self._assert_midi_message(msg3, 0x90, 72)

if __name__ == "__main__":
    main()

