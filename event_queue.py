from queue import Queue

class EventQueue(Queue):
  def __init__(self):
    super().__init__()
  
  def put(self, event, event_type=None, **kwargs):
    if isinstance(event, Event):
      super().put(event)
    else:
      super().put(
        Event(event, event_type, **kwargs)
      )

class Event(object):
  def __init__(self, item, event_type, **kwargs):
    self.type = event_type
    self.item = item
    self.timestamp = kwargs.get('timestamp')