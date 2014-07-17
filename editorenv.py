class EditorEnv:
  def __init__(self):
    self.buf = ''
    self.cursorv = 0
    self.cursorh = 0
  def clearbuf(self):
    self.buf = ''
  def loadbuf(self):
    pass
