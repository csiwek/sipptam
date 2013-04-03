from pysimplesoap.server import SoapDispatcher, SOAPHandler
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import time
import threading
import random
import logging

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    '''
    Handle requests in a separate thread.
    '''
    lock = None
    ports = None

    def __init__(self, address, ports, _handler):
        HTTPServer.__init__ (self, address, _handler)
        s = 'http://%s:%s/' % address
        self.dispatcher = SoapDispatcher(
            'my_dispatcher_%s%s' % address,
            location = s,
            action = s, # SOAPAction
            namespace = s,
            prefix="ns0",
            trace = True,
            ns = True,
            exceptions = True)
        self.dispatcher.register_function('getPort', self.getPort,
                                          returns={'port': int}, 
                                          args={'notused': int})
        self.dispatcher.register_function('runSipp', self.runSipp,
                                          returns={'pid': int}, 
                                          args={'r': int,
                                                'm': int,
                                                'sf': str,
                                                'inf' : str,
                                                'host': str,
                                                'port' : int,
                                                'p' : int})
        self.dispatcher.register_function('checkSuccess', self.checkSuccess,
                                          args={'pid': int}, 
                                          returns={'ret': int})
        self.dispatcher.register_function('checkFail', self.checkFail,
                                          args={'pid': int}, 
                                          returns={'ret': int})
        self.dispatcher.register_function('turnOff', self.turnOff,
                                          args={'pid': int}, 
                                          returns={'ret': int})
        self.dispatcher.register_function('hasFinish', self.hasFinish,
                                          args={'pid': int}, 
                                          returns={'ret': int})
        self.lock = threading.Lock()
        self.ports = ports

    def getPort(self, notused):
        with self.lock:
            item = -1
            try: 
                item = self.ports.pop()
            except:
                pass
        return item

    def runSipp(self, r, m, sf, inf, host, port, p):
        print r
        print m
        print sf
        print inf
        print host
        print port
        print p
        # (sudo sipp -sf $SCEN/$2.xml -inf $USRS $HOST_B2BUA:$PORT -p $BIND_PORT -r $3 -m $4 -trace_err)
        return 19009

    def checkSuccess(self, pid):
        return 222

    def checkFail(self, pid):
        return 111

    def turnOff(self, pid):
        return 1

    def hasFinish(self, pid):
        if random.randint(0, 100) > 20:
            return 0
        else:
            return 1


def https((host, port, ports)):
    server = ThreadingHTTPServer((host, port), ports, SOAPHandler)
    print "Starting server... in %s %s" % (host, port)
    server.serve_forever()

servers = [('localhost', 8008, range(7000, 8000)), 
           ('localhost', 8009, range(8000, 9000)),
           ('localhost', 8010, range(9000, 10000))]
#servers = [('localhost', 8008, range(7000, 8000))]
#servers = [('localhost', 8008)]
for s in servers:
    t = threading.Thread(target=https, args=[s,])
    t.daemon = True
    t.start()

while True:
    pass
