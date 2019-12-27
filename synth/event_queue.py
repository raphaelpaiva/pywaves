from queue import Queue

class EventQueue(Queue):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
  
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
    self.ancestor = kwargs.get('ancestor')
  
  def __str__(self):
    timestamp = f'{self.timestamp}, ' if self.timestamp else ''
    ancestor = str(self.ancestor) if self.ancestor else ''
    
    return f"{self.type}({str(self.item)} {timestamp} {ancestor})"

DUMMY_EVT = Event(None, None)