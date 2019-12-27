class Parameter(object):
  """ A parameter[name, relative_value]. relative_value is a float between 0 and 1 where 0 is minimum and 1 is maximum value. For absolute values (defined by min_value and max_value), use get(). """
  def __init__(self, name, min_value=0.0, max_value=1.0, init_value=0.5, label_format=None):
    super().__init__()
    
    self.name = name
    
    self.relative_value = init_value
    self.max_value      = max_value
    self.min_value      = min_value
    self.label_format   = label_format

  def get(self):
    """ Returns the absolute value of this parameter, based on the minimum and maximum values. """
    return self.relative_value * (self.max_value - self.min_value) + self.min_value
  
  def get_relative(self):
    return self.relative_value

  def set_relative(self, new_value):
    """ Sets the relative value [0,1] where 0 is minumum and 1 is maximum. """
    if new_value < 0.0:
      self.relative_value = 0.0
    elif new_value > 1.0:
      self.relative_value = 1.0
    else:
      self.relative_value = new_value
