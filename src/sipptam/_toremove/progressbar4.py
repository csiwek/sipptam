import time
import curses

def pbar(window):
    for i in range(10):
        window.addstr(10, 0, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.addstr(11, 2, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.addstr(12, 4, "[" + ("=" * i) + "+" + (" " * (10 - i )) + "]")
        window.refresh()
        time.sleep(0.5)

curses.wrapper(pbar)
