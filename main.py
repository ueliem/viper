#!/usr/bin/python
import curses, traceback, argparse, os
# from modes import *
from editorenv import *

def is_chr(possible):
    if possible < 256:
        return True
    return False

def cleanupcurses(stdscr):
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def registermode(mode):
    return mode

@registermode
def inputMode(stdscr, edenv):
    # stdscr.addstr(5, 0, "Edit mode")
    event = stdscr.getch()
    if event == 27:
        # modeman.set_mode("nrmlmode")
        pass
    if event == curses.KEY_UP:
        # edenv.topmostlinenum -= 1
        if edenv.cursorvert - edenv.topmostlinenum == 0:
            edenv.topmostlinenum -= int(curses.LINES/2)
        edenv.cursorvert -= 1
    elif event == curses.KEY_DOWN:
        # edenv.topmostlinenum += 1
        if edenv.cursorvert == (edenv.topmostlinenum + curses.LINES) - 1:
            edenv.topmostlinenum += int(curses.LINES/2)
        edenv.cursorvert += 1
    elif event == curses.KEY_LEFT:
        edenv.cursorhori -= 1
    elif event == curses.KEY_RIGHT:
        edenv.cursorhori += 1
    elif is_chr(event):
        edenv.buf += chr(event)
        # stdscr.addstr(0,0, mybuf)
    edenv.bottommostlinenum = (edenv.topmostlinenum + curses.LINES) - 1
    stdscr.erase()
    for (index, line) in enumerate(edenv.buf.split("\n")[edenv.topmostlinenum:edenv.bottommostlinenum]):
        stdscr.addstr(index, 0, line)
    stdscr.move(edenv.cursorvert - edenv.topmostlinenum, edenv.cursorhori)

def main(stdscr, edenv):
    dimensions = stdscr.getmaxyx()
    # modeman = ModeManager()
    # modeman.add_mode(NormalMode())
    # modeman.add_mode(InputMode())
    # modeman.set_mode("inpmode")
    if edenv.buf != None:
        edenv.bottommostlinenum = (edenv.topmostlinenum + curses.LINES) - 1
        for (index, line) in enumerate(edenv.buf.split("\n")[edenv.topmostlinenum:edenv.bottommostlinenum]):
                stdscr.addstr(index, 0, line)
        stdscr.refresh()
    while True:
        # if modeman.current_mode.mode_id == "inpmode":
        if not inputMode(stdscr, edenv):
            #switch state, or break
            pass
        # elif modeman.current_mode.mode_id == "nrmlmode":
        #     event = stdscr.getch()
        #     if event == ord("q"): break
        #     elif event == ord("i"):
        #         modeman.set_mode("inpmode")
        stdscr.refresh()

if __name__=='__main__':
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        # curses.curs_set(0)
        stdscr.keypad(1)
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        # curses.curs_set(0)
        stdscr.keypad(1)
        stdscr.refresh()
        parser = argparse.ArgumentParser(description='Viper.')
        parser.add_argument('file', type=file, nargs='?', default=None, help='')
        args = parser.parse_args()
        edenv = EditorEnv()
        if args.file:
            path = os.path.abspath(args.file.name)
            edenv.buf = open(path).read()
        edenv.topmostlinenum = 0
        edenv.bottommostlinenum = (edenv.topmostlinenum + curses.LINES) - 1
        edenv.cursorvert = 0
        edenv.cursorhori = 0
        main(stdscr, edenv)
        cleanupcurses(stdscr)
    except:
        cleanupcurses(stdscr)
        traceback.print_exc()
