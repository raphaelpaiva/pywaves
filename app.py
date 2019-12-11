import time
import threading
import argparse
import logging
import midi
import psutil

from interface import (CLInterface, TkInterface)
from input.keyboardInput import (KeyboardInput, EVT_KEY, EVT_KEY_PRESSED, EVT_KEY_RELEASED)
from event_queue import (EventQueue, Event)
from synth import Synth

from observer import Observer

LOGGER_NAME = 'app'
interface_map = {
  'cli': CLInterface,
  'tk': TkInterface
}

EVT_SYS = 'sys_'
EXIT_ITEM = 'exit'
EXIT_KEY = 'esc'

EXIT_EVENT = Event(EXIT_ITEM, EVT_SYS)

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

event_type_midi_action = {
  EVT_KEY_PRESSED: midi.note_on,
  EVT_KEY_RELEASED: midi.note_off
}

class App(object):
  def __init__(self, Iface, arguments, *args, **kwargs):
    super(App).__init__(*args, **kwargs)
    
    self.args = arguments
    self.stop = False
    self.log = logging.getLogger(LOGGER_NAME)

    self.process = psutil.Process()
    self.process.cpu_percent() # required first call
    self.observer = Observer()
    self.observer.add('app', self)
    self.observer_thread = threading.Thread(target=self._observer_loop, name="Observer")
    self.observer_thread.start()

    self.log.debug('Initializing Input...')
    self._init_input()
    
    self.log.debug('Initializing synth...')
    self._init_synth()

    self.log.debug('Initializing Interface...')
    self.IfaceType = Iface
    self._init_interface()

  def _init_input(self):
    self.input_queue = EventQueue()
    self.input = KeyboardInput(self.input_queue)
    self.input.start()
    
    self.input_thread = threading.Thread(target=self._process_input_queue, name="input_queue")
    self.input_thread.start()

  def _process_input_queue(self):
    while not self.stop:
      event = self.input_queue.get() # Blocking
      
      self.log.debug(f'Got event {event}')

      item = event.item

      if event.type.startswith(EVT_SYS):
        if item == EXIT_ITEM:
          self._terminate()
      
      if event.type.startswith(EVT_KEY):
        if item in keyboard_note_table:
          note, octave = keyboard_note_table[item]

          new_event = Event(
            event_type_midi_action[event.type](note, octave, 127),
            midi.EVT_MIDI,
            ancestor=event,
            timestamp=time.time()
          )

          self.synth_queue.put(new_event)
        else:
          if item == EXIT_KEY:
            self.input_queue.put(
              Event(
                EXIT_ITEM,
                EVT_SYS,
                ancestor=event,
                timestamp=time.time()
              )
            )

    self.log.debug('Exiting input Thread loop...')

  def _init_interface(self):
    self.interface = self.IfaceType(self.synth, log=self.log, debug=self.args.debug)
    self.interface.start(exit_action=self.exit)
  
  def _init_synth(self):
    self.synth = Synth(log=self.log)
    self.synth_queue = self.synth.event_queue

  def _terminate(self):
    self.log.debug("Terminating app...")
    self.stop = True
    
    self.log.debug("Terminating Input...")
    self.input.stop()

    self.log.debug("Terminating Synth...")
    self.synth.terminate()

    if threading.get_ident() != self.input_thread.ident:
      self.log.debug('Stopping input Thread...')
      self.input_thread.join()

    self.log.debug("Terminating Interface...")
    self.interface.stop()

    self.log.debug("Terminating Observer Thread...")
    self.observer_thread.join()

    self.log.debug("Finished terminating app!")
  
  def exit(self):
    self.input_queue.put(EXIT_EVENT)

  def _observer_loop(self):
    while not self.stop:
      print(self.observer.observe())
      time.sleep(2.0)

  def observe(self):
    p = self.process
    with p.oneshot():
      return {
        'pid': p.pid,
        'name': p.name(),
        'cpu_percent': p.cpu_percent() / psutil.cpu_count(),
        'num_threads': p.num_threads(),
        'threads': p.threads(),
        'memory': float(p.memory_info().rss / (1024 * 1024)),
        'memory_percent': p.memory_percent(),
      }

def main():
  args = parse_args()
  log = init_log(args)
  Iface = get_interface_type(args)
  log.debug(f'Using {Iface} as the interface type')
  
  log.debug(f'Initializing App...')
  App(Iface, args)
  log.debug(f'Bye ;)')

def get_interface_type(args):
  return interface_map[args.interface]

def init_log(args):
  if args.debug:
    logging.basicConfig(
      level=logging.DEBUG,
      format="%(asctime)s [%(name)s (%(threadName)s)] %(levelname)s: %(message)s",
      datefmt="%d/%m/%Y %H:%M:%S"
    )

  log = logging.getLogger(f'{LOGGER_NAME}.init')
  log.debug('Oh, hello there! ;)')

  return log

def parse_args():
  parser = argparse.ArgumentParser(description="I'm a poor synth")
  
  parser.add_argument(
    '--debug',
    help="enables debug log",
    action='store_true'
  )
  parser.add_argument(
    '-i', '--interface',
    help="interface type",
    choices=interface_map.keys(),
    default='tk'
  )

  return parser.parse_args()

if __name__ == "__main__":
  main()