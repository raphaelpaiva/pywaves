import random
import string

from threading import Thread
from time import sleep
import queue
from queue import Queue as EventQueue

class Module(object):
  def __init__(self, name: str):
    super().__init__()
    self.name = name
    self.input = EventQueue()
    self.output = Connection()
    self.do_stop = False
  
  def start(self): pass

  def run(self): pass

  def stop(self):
    self.do_stop = True

class ThreadModule(Module):
  def __init__(self, name: str):
    super().__init__(name)
    self.thread = Thread(target=self.run, name=f'thread-{self.name}')

  def run(self): pass

  def start(self):
    self.thread.start()
  
  def stop(self):
    super().stop()
    self.thread.join()

class PrintModule(ThreadModule):
  def __init__(self, name: str):
    super().__init__(f'Print[{name}]')
  
  def run(self):
    while not self.do_stop:
      try:
        obj = self.input.get(timeout=1.0)
        print(f'{self.name}:: {obj}')
        self.input.task_done()
      except queue.Empty: pass

class RandomModule(ThreadModule):
  def __init__(self, name: str):
    super().__init__(name)
  
  def run(self):
    while not self.do_stop:
      letters = string.ascii_letters
      gen = ''.join(random.choice(letters) for i in range(random.randrange(4,15)))
      self.output.put(gen)
      sleep(random.random() * 5)

class Connection(EventQueue):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.outputs = []

  def put(self, *args, **kwargs):
    for output in self.outputs:
      output.input.put(*args, **kwargs)
  
  def connect(self, module: Module):
    self.outputs.append(module)
