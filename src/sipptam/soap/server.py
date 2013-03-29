from pysimplesoap.server import SoapDispatcher, SOAPHandler
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import time
import threading

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
                                          returns={'summ': int}, 
                                          args={'param': int})
        self.lock = threading.Lock()
        self.ports = ports

    def getPort (self, param):
        with self.lock:
            try: 
                item = self.ports.pop()
            except:
                item = 0
        return item

def https((host, port, ports)):
    server = ThreadingHTTPServer((host, port), ports, SOAPHandler)
    print "Starting server... in %s %s" % (host, port)
    server.serve_forever()

servers = [('localhost', 8008, range(7000, 8000)), 
           ('localhost', 8009, range(8000, 9000)),
           ('localhost', 8010, range(9000, 10000))]
#servers = [('localhost', 8008)]
for s in servers:
    t = threading.Thread(target=https, args=[s,])
    t.daemon = True
    t.start()

while True:
    pass
