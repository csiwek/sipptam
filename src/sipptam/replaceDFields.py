import re
import sys
import glob
import os
import random

tas = dict([(x, ('911%s' % (x*random.randint(1, 10)), '10.22.22.%s' % x)) for x in range(0, 1000)])

def replaceDFields(tmp):
    regex = r"!sipptas\((?P<name>port|host)\((?P<number>\d+)\)\)!"
    for name, number in re.findall(regex, tmp):
        port, host = tas[int(number)]
        if 'port' == name: dest = port
        elif 'host' == name: dest = host
        ori = ('!sipptas(%s(%s))!' % (name, number))
        print 'Replacing : %s ---> %s' % (ori, dest)

# Doing some testing
tests = ['Refer-To: sip:refered_user@!sipptas(host(3))!:!sipptas(port(3))!;another_opts=True']
for test in tests:
    print 'Doing test... \"%s\"' % test
    replaceDFields(test)
    print '-' * 30

flist = glob.glob('/Volumes/lmartin_data/sipptam/resources/scenarios/test-d0020-*.xml')
for fn in flist:
    print 'Working with file... \"%s\"' % os.path.basename(fn)
    f = open(fn)
    tmp = f.read()
    replaceDFields(tmp)
    print '-' * 30

