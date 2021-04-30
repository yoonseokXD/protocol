import sys
import binascii
from binascii import hexlify
key = [0xE9,0xF3,0x94,0x37,0x0A,0xD4,0x05,0x89,0x88,0xE3,0x4F,0x8F,0x08,0x17,0x79,0xF1]
dec_key = [233, 243, 148, 55, 10, 212, 5, 137, 136, 227, 79, 143, 8, 23, 121]
key_hex = ['0xe9', '0xf3', '0x94', '0x37', '0xa', '0xd4', '0x5', '0x89', '0x88', '0xe3', '0x4f', '0x8f', '0x8', '0x17']
FX = [0xF6,0x3E,0x98,0x78,0xDE,0x73,0x33,0x86,0xA8,0x00,0xE1,0x1D,0xBB,0xA7,0x79,0x2F]
bin_key = []
default_key = 'E9 F3 94 37 0A D4 05 89 88 E3 4F 8F 08 17 79 F1'.encode()
default_key = ['E9','F3', '94', '37', '0A', 'D4', '05', '89', '88', 'E3', '4F', '8F', '08', '17', '79', 'F1']

data_header = 'TUPG110000100156'
data_body = '2.030547501027887948d5bb3912933b09476d69f434e260f96aca3a60829877c6dd78b0'

h = []
for x in range(0, len(key_hex)-1, +1):
	i = bin(dec_key[x])
	bin_key.append(i)
aschex = " ".join([hex(ord(x)) for x in data_header])
print(aschex)
hex_ls=[x.replace('0x','0') if len(x)<4 else x.replace('0x','') for x in aschex.split(" ")]
print(hex_ls)
hex_lsj = ''.join(hex_ls)
print(hex_lsj)
rm0x = [f"{i:1>2}" for i in aschex]

'''
i = int(h, 16)
print(i)
print(type(0xE9))
print(sys.getsizeof(byte_key))'''