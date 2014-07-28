import curses

class EditorEnv:
    def __init__(self):
        self.buffers = []
        self.current_buffer_index = 0
        # self.bufname = None
        # self.stdscr = stdscr
        # self.cursorv = 0
        # self.cursorh = 0
        # self.topmostlinenum
        # self.bottommostlinenum
    def clearbuf(self):
        self.buf = ""
    def loadbuf(self, freshbuffer):
        self.buffers.append(freshbuffer)
    def next_buf(self):
        if current_buffer_index - 1 >= 0:
            current_buffer_index -= 1
    def prev_buf(self):
        if current_buffer_index + 1 < len(self.buffers):
            current_buffer_index += 1
    def current_buffer(self):
        return self.buffers[self.current_buffer_index]

class Buffer:
    def __init__(self, buf="", name=None):
        self.buf = buf
        self.name = name
