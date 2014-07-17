class Mode:
    def __init__(self):
        self.mode_id = None
    def on_frame(self):
        pass

class InputMode(Mode):
    def __init__(self):
        self.mode_id = "inpmode"
        self.cursorv = 0
        self.cursorh = 0

class NormalMode(Mode):
    def __init__(self):
        self.mode_id = "nrmlmode"
    def on_frame(self):
        pass

class ModeManager:
    def __init__(self):
        self.modes = {}
        self.current_mode = None
    def add_mode(self, mode):
        self.modes[mode.mode_id] = mode
    def set_mode(self, mode_id):
        self.current_mode = self.modes[mode_id]
