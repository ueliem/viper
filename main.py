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
    # stdscr.addstr(edenv.dimensions[0] - 1, 0, "Edit mode")
    needstomovevert = 0
    event = stdscr.getch()
    if event == 27:
        # modeman.set_mode("nrmlmode")
        pass
    if event == curses.KEY_UP:
        needstomovevert = -1
        # edenv.oldcursorvert = edenv.cursorvert
        # edenv.cursorvert -= 1
    elif event == curses.KEY_DOWN:
        needstomovevert = 1
        # edenv.oldcursorvert = edenv.cursorvert
        # edenv.cursorvert += 1
    elif event == curses.KEY_LEFT:
        edenv.cursorreal -= 1
    elif event == curses.KEY_RIGHT:
        # edenv.cursorhori += 1
        edenv.cursorreal += 1
    elif is_chr(event):
        edenv.current_buffer().buf = edenv.current_buffer().buf[:edenv.cursorreal] + chr(event) + edenv.current_buffer().buf[edenv.cursorreal:]
        edenv.cursorreal += 1
    edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
    stdscr.erase()
    lines = edenv.current_buffer().buf.split("\n")
    for (index, line) in enumerate(lines[edenv.topmostlinenum:edenv.bottommostlinenum]):
        stdscr.addstr(index, 0, line)
    charcount = 0
    for (index, line) in enumerate(lines):
        if edenv.cursorreal - (charcount) <= len(line):
            if needstomovevert < 0 and index > 0:
                if len(lines[index-1]) >= edenv.cursorhori:
                    edenv.cursorreal -= (len(lines[index-1]) + 1)
                else:
                    edenv.cursorreal -= (edenv.cursorhori) + 1
                edenv.cursorvert = (index - 1)
                edenv.cursorhori = (edenv.cursorreal - (charcount) + len(lines[index-1]) + 1)
                if edenv.cursorhori > len(lines[index-1]): edenv.cursorhori = len(lines[index-1])
            elif needstomovevert > 0 and index < len(lines) - 1:
                if len(lines[index+1]) >= edenv.cursorhori:
                    edenv.cursorreal += (len(line) + 1)
                else:
                    edenv.cursorreal += (len(line) + 1)
                edenv.cursorvert = (index + 1)
                edenv.cursorhori = (edenv.cursorreal - (charcount) - len(line) - 1)
                if edenv.cursorhori > len(lines[index+1]): edenv.cursorhori = len(lines[index+1])
            else:
                edenv.cursorvert = (index)
                edenv.cursorhori = (edenv.cursorreal - (charcount))
            break
        else:
            charcount += len(line) + 1

    if edenv.cursorvert < 0: edenv.cursorvert = 0
    if edenv.cursorhori < 0: edenv.cursorhori = 0
    stdscr.move(edenv.cursorvert - edenv.topmostlinenum, edenv.cursorhori)

def main(stdscr, edenv):
    if edenv.current_buffer() != None:
        edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
        for (index, line) in enumerate(edenv.current_buffer().buf.split("\n")[edenv.topmostlinenum:edenv.bottommostlinenum]):
                stdscr.addstr(index, 0, line)
        stdscr.refresh()
    while True:
        if not inputMode(stdscr, edenv):
            #switch state, or break
            pass
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
            edenv.loadbuf(Buffer(open(path).read(), path))
        else:
            edenv.loadbuf(Buffer("", None))
        edenv.dimensions = stdscr.getmaxyx()
        edenv.topmostlinenum = 0
        edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
        edenv.cursorreal = 0
        edenv.cursorvert = 0
        edenv.cursorhori = 0
        edenv.oldcursorvert = 0
        main(stdscr, edenv)
        cleanupcurses(stdscr)
    except:
        cleanupcurses(stdscr)
        traceback.print_exc()
