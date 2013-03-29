from pysimplesoap.client import SoapClient, SoapFault
import Queue
import threading
from random import choice

class SoapPool(object):
    connections = None
    lock = None
    def __init__(self, generate, size=10):
        self.connections = [generate() for x in range(size)]
        self.lock = threading.Lock()
    def pop(self):
        item = None
        while not item:
            with self.lock:
                if len(self.connections):
                    item = self.connections.pop()
        return item
    def insert(self, c):
        with self.lock:
            self.connections.append(c)

def worker(q, sp):
    while True:
        item = q.get()
        client = sp.pop()
        try:
            response = client.getPort(param=item)
        except:
            raise
        else:
            print '%s\n' % response.summ
        sp.insert(client)
        q.task_done()

def fun(servers, jobs, size_soap_pool, n_workers):
    def generate():
        s = 'http://%s:%s/' % choice(servers)
        return SoapClient(
            location = s,
            action = s, # SOAPAction
            namespace = s, 
            soap_ns='soap', 
            trace = False, 
            ns = False, 
            exceptions = True)
    sp = SoapPool(generate, size=size_soap_pool)
    q = Queue.Queue()
    for i in range(n_workers):
        t = threading.Thread(target=worker, args=[q,sp,])
        t.daemon = True
        t.start()
    for item in range(jobs):
        q.put(item)
    q.join()

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    #servers = [('localhost', 8008)]
    servers = [('localhost', 8008), ('localhost', 8009), ('localhost', 8010)]
    jobs = 3000
    size_soap_pool = 20
    n_workers = 25
    
    fun(servers,
        jobs,
        size_soap_pool,
        n_workers)
