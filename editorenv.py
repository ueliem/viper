import curses

class EditorEnv:
    def __init__(self):
        self.buf = ''
        # self.bufname = None
        # self.stdscr = stdscr
        # self.cursorv = 0
        # self.cursorh = 0
        # self.topmostlinenum
        # self.bottommostlinenum
    def clearbuf(self):
        self.buf = ''
    def loadbuf(self, freshbuffer, bufname):
        self.buf = freshbuffer
        self.bufname = bufname
