from pysimplesoap.client import SoapClient


def getClient(host, port):
    s = 'http://%s:%s/' % (host, port)
    return SoapClient(
        location = s, 
        action = s, 
        namespace = s, 
        soap_ns='soap',
        trace = False, 
        ns = False, 
        exceptions = False)

if __name__ == '__main__':
    '''
    Main execution thread.
    '''
    import threading
    
    def test(host, port):
        a = getClient(host, port)
        response = a.getPort(param=22)
        print response.summ

    al = [threading.Thread(target=test, args=['localhost',8008,]) for _ in range(10)]
    
    for a in al:
        a.setDaemon(True)
        a.start()

    for a in al:
        a.join()
