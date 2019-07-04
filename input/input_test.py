from unittest import TestCase, main

from pynput.keyboard import Key, KeyCode
from collections import namedtuple
from queue import Queue
from input import KeyboardInput, EVT_KEY_PRESSED, EVT_KEY_RELEASED

class EventQueueMock(Queue):
  def __init__(self):
    super().__init__()
  
  def put(self, *args, **kwargs):
    EventMock = namedtuple('Event', ['item', 'type', 'timestamp'])
    super().put(EventMock(*args, **kwargs))

class KeyboardInputTest(TestCase):
  def _assert_queue_size(self, queue, expected_size=1):
    self.assertFalse(queue.empty(), "Expected the queue not to be empty")
    self.assertEqual(queue.qsize(), expected_size)

  def _assert_message(self, msg, expected_type, expected_key):
    self.assertEqual(msg.type, expected_type)
    self.assertEqual(msg.item, expected_key)

  def test_onpress_SpecialKeyShouldPutKeyInQueue(self):
    queue = EventQueueMock()
    key_pressed = Key.esc

    kb = KeyboardInput(queue)
    kb.onpress(key_pressed)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_message(msg, EVT_KEY_PRESSED, '<esc>')

  def test_onpress_OneKeyPressShouldCreateOneMidiOnMessage(self):
    queue = EventQueueMock()
    key_pressed = KeyCode.from_char('q')

    kb = KeyboardInput(queue)
    kb.onpress(key_pressed)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_message(msg, EVT_KEY_PRESSED, 'q')

  def test_onpress_KeepPressingAKeyShouldPutOnlyOneNoteOnMessageOnTheQueue(self):
    queue = EventQueueMock()
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

    self._assert_message(msg, EVT_KEY_PRESSED, 'y')

  def test_onrelease_OneKeyPressShouldCreateOneMidiOnMessage(self):
    queue = EventQueueMock()
    key_released = KeyCode.from_char('q')

    kb = KeyboardInput(queue)
    kb.onrelease(key_released)

    self._assert_queue_size(queue)

    msg = queue.get()

    self._assert_message(msg, EVT_KEY_RELEASED, 'q')

  def test_onrelease_SpecialKeyShouldNotPutKeyInQueue(self):
    queue = EventQueueMock()
    key_released = Key.esc

    kb = KeyboardInput(queue)
    kb.onrelease(key_released)

    self.assertTrue(queue.empty(), "Expected the queue to be empty")

  # Testing a bug (Issue #1)
  def test_pressReleasePress_shouldNotBlockTheLastPress(self):
    queue = EventQueueMock()
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

    self._assert_message(msg1, EVT_KEY_PRESSED, 'y')
    self._assert_message(msg2, EVT_KEY_RELEASED, 'y')
    self._assert_message(msg3, EVT_KEY_PRESSED, 'y')

if __name__ == "__main__":
    main()

