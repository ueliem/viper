#!/usr/bin/python
import curses, traceback, argparse, os, sys
# from modes import *
from editorenv import *

def tokenize_command_structure(commandstring):
    startstate = 0
    numstate = 1
    wordstate = 2
    commastate = 3
    curstate = startstate
    tokenstack = []
    charstack = []
    for c in commandstring:
        if curstate == startstate:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                charstack.append(c)
                curstate = numstate
            elif c in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                charstack.append(c)
                curstate = wordstate
            elif c == ',':
                charstack.append(c)
                curstate = commastate
            elif c == ' ':
                continue
        elif curstate == numstate:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                charstack.append(c)
            elif c in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = wordstate
            elif c == ',':
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = commastate
            elif c == ' ':
                tokenstack.append("".join(charstack))
                charstack = []
        elif curstate == wordstate:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = numstate
            elif c in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                charstack.append(c)
            elif c == ',':
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = commastate
            elif c == ' ':
                tokenstack.append("".join(charstack))
                charstack = []
        elif curstate == commastate:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = numstate
            elif c in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'):
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = wordstate
            elif c == ',':
                tokenstack.append("".join(charstack))
                charstack = []
                charstack.append(c)
                curstate = commastate
            elif c == ' ':
                tokenstack.append("".join(charstack))
                charstack = []
    tokenstack.append("".join(charstack))
    return tokenstack

def parse_command_tokens(edenv, tokens):
    if tokens[0] in custom_commands:
        custom_commands[tokens[0]](edenv)
    elif tokens[0] in default_commands:
        default_commands[tokens[0]](edenv)

def quit(edenv):
    # TODO check for file changes
    sys.exit(0)

def writebuffertofile(edenv, filename=None):
    if edenv.current_buffer().buf and filename == None and edenv.current_buffer().name:
        target = open(edenv.current_buffer().name, 'w')
        target.write(edenv.current_buffer().buf)
        target.close()
    elif edenv.current_buffer().buf and filename != None:
        target = open(filename, 'w')
        target.write(edenv.current_buffer().buf)
        target.close()

def writethenquit(edenv, filename=None):
    writebuffertofile(edenv, filename)
    quit(edenv)

default_commands = {
    "q" : quit,
    "quit" : quit,
    "w" : writebuffertofile,
    "wq" : writethenquit
}

custom_commands = {}

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

def parse_command(edenv, command):
    parse_command_tokens(edenv, tokenize_command_structure(command))

@registermode
def normalMode(stdscr, edenv):
    # TODO Add ability to move through file in this mode
    event = stdscr.getch()
    if event == 10:
        parse_command(edenv, edenv.commandbuf[1:])
        edenv.commandbuf = ""
    elif event == 8 or event == 127:
        edenv.commandbuf = edenv.commandbuf[:len(edenv.commandbuf)-1]
    elif is_chr(event) and chr(event) == ":":
        edenv.commandbuf += ":"
    elif is_chr(event) and len(edenv.commandbuf) > 0 and edenv.commandbuf[0] == ":":
        edenv.commandbuf += chr(event)
    stdscr.erase()
    lines = edenv.current_buffer().buf.split("\n")
    for (index, line) in enumerate(lines[edenv.topmostlinenum:edenv.bottommostlinenum]):
        stdscr.addstr(index, 0, line)
    stdscr.addstr(edenv.dimensions[0] - 1, 0, edenv.commandbuf)

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
        if not normalMode(stdscr, edenv):
            # TODO switch state, or break
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
            openedfile = open(path)
            edenv.loadbuf(Buffer(openedfile.read(), path))
            openedfile.close()
        else:
            edenv.loadbuf(Buffer("", None))
        edenv.dimensions = stdscr.getmaxyx()
        edenv.topmostlinenum = 0
        edenv.bottommostlinenum = (edenv.topmostlinenum + edenv.dimensions[0]) - 1
        edenv.cursorreal = 0
        edenv.cursorvert = 0
        edenv.cursorhori = 0
        edenv.oldcursorvert = 0
        edenv.commandbuf = ""
        main(stdscr, edenv)
        cleanupcurses(stdscr)
    except:
        cleanupcurses(stdscr)
        traceback.print_exc()
