import gi
import time, threading

from gi.repository import GObject

class GArray(GObject.GObject):
    def __init__(self):
        super().__init__()

        self.list = []

    def append(self, obj: object):
        self.list.append(obj)

    def remove(self, obj: object):
        self.list.remove(obj)

    def find(self, obj):
        try:
            return self.list.index(obj)
        except ValueError:
            return -1

StartTime=time.time()

def action() :
    print('action ! -> time : {:.1f}s'.format(time.time()-StartTime))

class setInterval :
    def __init__(self,interval, callback) :
        self.interval=interval
        self.action=callback
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action(self)

    def cancel(self) :
        self.stopEvent.set()

class setTimeout:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.cb = callback
        threading.Thread(target=self.__timeout()).start()

    def __timeout(self):
        time.sleep(self.timeout)
        self.cb()
