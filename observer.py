class Observer(object):
  def __init__(self):
    super().__init__()

    self._observed = {}

  def add(self, name, obj):
    self._observed[name] = obj
  
  def observe(self):
    state_map = {}
    
    for name, obj in self._observed.items():
      if hasattr(obj, 'observe') and callable(obj.observe):
        state_map[name] = obj.observe()
      else:
        state_map[name] = str(obj)
    
    return state_map