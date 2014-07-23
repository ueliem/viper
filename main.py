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

# def cursor_is_at_buf_end(cursorhori, cursorvert, buflen):

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
        # if edenv.cursorvert - edenv.topmostlinenum == 0:
        #     edenv.topmostlinenum -= int(curses.LINES/2)
        # edenv.cursorvert -= 1
        pass
    elif event == curses.KEY_DOWN:
        # edenv.topmostlinenum += 1
        # if edenv.cursorvert == (edenv.topmostlinenum + curses.LINES) - 1:
        #     edenv.topmostlinenum += int(curses.LINES/2)
        # edenv.cursorvert += 1
        pass
    elif event == curses.KEY_LEFT:
        edenv.cursorreal -= 1
    elif event == curses.KEY_RIGHT:
        edenv.cursorreal += 1
    elif is_chr(event):
        # edenv.buf += chr(event)
        # stdscr.addstr(0,0, mybuf)
        edenv.buf = edenv.buf[:edenv.cursorreal] + chr(event) + edenv.buf[edenv.cursorreal:]
        edenv.cursorreal += 1
    edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
    stdscr.erase()
    numlines = 0
    numcols = edenv.cursorreal
    lines = edenv.buf.split("\n")
    # numlines += (len(lines) - 1)
    numcolsset = False
    for (index, line) in enumerate(lines[edenv.topmostlinenum:edenv.bottommostlinenum]):
        stdscr.addstr(index, 0, line)
        if index == 0:
            # if numcols < edenv.dimensions[1]:
            if numcols <= len(line):
                if not numcolsset:
                    edenv.cursorhori = numcols
                    edenv.cursorvert = numlines
                    numcolsset = True
                continue
            else:
                numcols -= len(line)
                # numlines += 1
        else:
            if numcols <= len(line):
                if not numcolsset:
                    edenv.cursorhori = numcols
                    edenv.cursorvert = numlines
                    numcolsset = True
                continue
            else:
                numcols -= len(line) + 1
                numlines += 1
    edenv.cursorvert = numlines
    edenv.cursorhori = numcols
    stdscr.move(edenv.cursorvert - edenv.topmostlinenum, edenv.cursorhori)
    # stdscr.move(0, edenv.cursorreal)

def main(stdscr, edenv):
    # modeman = ModeManager()
    # modeman.add_mode(NormalMode())
    # modeman.add_mode(InputMode())
    # modeman.set_mode("inpmode")
    if edenv.buf != None:
        edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
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
        edenv.dimensions = stdscr.getmaxyx()
        edenv.topmostlinenum = 0
        edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
        edenv.cursorreal = 0
        edenv.cursorvert = 0
        edenv.cursorhori = 0
        main(stdscr, edenv)
        cleanupcurses(stdscr)
    except:
        cleanupcurses(stdscr)
        traceback.print_exc()
