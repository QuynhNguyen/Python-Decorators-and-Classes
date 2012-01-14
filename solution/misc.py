def compose(f, g):
  def h(x):
    return f(g(x))
  return h

class Failure(Exception):
    """Failure exception"""
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)
