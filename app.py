import argparse
import logging
import threading

from interface import (CLInterface, TkInterface)
from synth import Synth

LOGGER_NAME = 'app'
interface_map = {
  'cli': CLInterface,
  'tk': TkInterface
}
class App(object):
  def __init__(self, Iface, *args, **kwargs):
    super(App).__init__(*args, **kwargs)
    self.log = logging.getLogger(LOGGER_NAME)
    
    self.log.debug('Initializing synth...')
    self._init_synth()
    
    self.log.debug('Initializing Interface...')
    self.IfaceType = Iface
    self._init_interface()
    
    self.queue_thread.join()
    self.synth.terminate()

  def _init_interface(self):
    self.interface = self.IfaceType(self.synth)
    self.interface.start()
  
  def _init_synth(self):
    self.synth = Synth()
    self.queue_thread = threading.Thread(target=self.synth.process_queue)
    self.queue_thread.start()

def main():
  args = parse_args()
  log = init_log(args)
  Iface = get_interface_type(args)
  log.debug(f'Using {Iface} as the interface type')
  
  log.debug(f'Initializing App...')
  App(Iface)


def get_interface_type(args):
  return interface_map[args.interface]

def init_log(args):
  if args.debug:
    logging.basicConfig(
      level=logging.DEBUG,
      format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
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
    default='cli'
  )

  return parser.parse_args()



if __name__ == "__main__":
  main()