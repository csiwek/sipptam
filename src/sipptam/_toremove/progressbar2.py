## {{{ http://code.activestate.com/recipes/577871/ (r1)
import sys
import time
import random
import curses

class ProgressBar(object):
    """ProgressBar class holds the options of the progress bar.
    The options are:
        start   State from which start the progress. For example, if start is 
                5 and the end is 10, the progress of this state is 50%
        end     State in which the progress has terminated.
        width   --
        fill    String to use for "filled" used to represent the progress
        blank   String to use for "filled" used to represent remaining space.
        format  Format
        incremental
    """
    def __init__(self, desc=None, start=0, end=10, 
                 width=12, fill='=', blank='.',
                 format='%(desc)s [%(fill)s>%(blank)s] %(progress)2s%%', 
                 incremental=True):
        super(ProgressBar, self).__init__()
        self.desc = desc
        self.start = start
        self.end = end
        self.width = width
        self.fill = fill
        self.blank = blank
        self.format = format
        self.incremental = incremental
        self.step = 100 / float(width) #fix
        self.reset()

    def __add__(self, increment):
        increment = self._get_progress(increment)
        if 100 > self.progress + increment:
            self.progress += increment
        else:
            self.progress = 100
        return self

    def __str__(self):
        progressed = int(self.progress / self.step) #fix
        fill = progressed * self.fill
        blank = (self.width - progressed) * self.blank
        return self.format % {'desc' : self.desc, 
                              'fill': fill, 
                              'blank': blank, 
                              'progress': int(self.progress)}

    __repr__ = __str__

    def _get_progress(self, increment):
        return float(increment * 100) / self.end

    def reset(self):
        """Resets the current progress to the start point"""
        self.progress = self._get_progress(self.start)
        return self

    def isCompleted(self):
        """ ... """
        return self.progress >= self.end


class ListProgressBar(object):
    l = None
    def __init__(self, l):
        self.l = l
    def draw(self):
        ret = []
        for i in self.l:
            ret.append('%s' % i)
        curses.echo()
        curses.nocbreak()
        sys.stdout.write('\n\r'.join(ret))
        curses.endwin()


    
if __name__ == '__main__':
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    p1 = ProgressBar(desc="test-000-1.xml", end=100, width=10)
    p2 = ProgressBar(desc="test-000-2.xml", end=100, width=10)
    p3 = ProgressBar(desc="test-000-3.xml", end=100, width=10)
    lp = ListProgressBar ([p1, p2, p3])
    
    while True:
        p1 + random.randint(1, 9)
        p2 + random.randint(1, 8)
        p3 + random.randint(1, 7)
        time.sleep(0.1)
        try:
            lp.draw()
            if all(map(lambda x: x.isCompleted(), lp.l)):
                break
        finally:
            curses.echo()
            curses.nocbreak()
            curses.endwin()
