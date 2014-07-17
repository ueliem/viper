#!/usr/bin/python
import curses, traceback
from modes import *
from editorenv import *

def is_chr(possible):
  if possible < 256:
    return True

def main(stdscr):
  dimensions = stdscr.getmaxyx()

  mybuf = ''

  modeman = ModeManager()
  modeman.add_mode(NormalMode())
  modeman.add_mode(InputMode())
  modeman.set_mode("inpmode")
  topmostlinenum = 0
  while True:
    if modeman.current_mode.mode_id == "inpmode":
      # stdscr.addstr(5, 0, "Edit mode")
      event = stdscr.getch()
      if event == 27:
        modeman.set_mode("nrmlmode")
      if event == curses.KEY_UP:
        topmostlinenum -= 1
      elif event == curses.KEY_DOWN:
        topmostlinenum += 1

      if is_chr(event):
        mybuf += chr(event)
      # stdscr.addstr(0,0, mybuf)
      bottommostlinenum = topmostlinenum + curses.LINES
      stdscr.erase()
      for (index,line) in enumerate(mybuf.split("\n")[topmostlinenum:bottommostlinenum]):
        stdscr.addstr(index, 0, line)

    elif modeman.current_mode.mode_id == "nrmlmode":
      event = stdscr.getch()
      if event == ord("q"): break
      elif event == ord("i"):
        modeman.set_mode("inpmode")
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
    main(stdscr)

    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
  except:
    stdscr.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    traceback.print_exc()
