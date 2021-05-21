import sys, queue
from collections import deque


__version__ = '1.0.0'
'''
key = [0xE9,0xF3,0x94,0x37,0x0A,0xD4,0x05,0x89,0x88,0xE3,0x4F,0x8F,0x08,0x17,0x79,0xF1]
key_b = [0x88,0xE3,0x4F,0x8F,0x08,0x17,0x79,0xF1,0xE9,0xF3,0x94,0x37,0x0A,0xD4,0x05,0x89]
key_b2 = [0x26,0x8D,0x66,0xA7,0x35,0xA8,0x1A,0x81,0x6F,0xBA,0xD9,0xFA,0x36,0x16,0x25,0x01]
sp = []
for i in range(0, len(key)-1, +1) :
	key_b.append(bin(key[i]))
	key_b2.append(key_b[i].replace("0b", ""))
			

iv = b'6FBAD9FA36162501268D66A735A81A81'
s = frozenset([128])
print(sys.getsizeof(s))
print(len(s))

print("key list size : ", len(key))
print("key b :" , key_b)



print(key_b2)

key_b3 = "".join(key_b2)
print(key_b3)
print(len(key_b3))
key_b4 = list(key_b3)
print(key_b4, len(key_b4))


if len(key_b2[i]) < 8 :
		for i in range(0, (len(key_b2)-1),+1):
			if len(key_b2[i]) < 8 :
				deq.appendleft(0)


fin = ['11101001', '11110011', '10010100', '00110111', '00001010', '11010100', '00000101', '10001001', '10001000', '11100011', '01001111', '10001111', '00001000', '00010111', '01111001', '11110001']
fin_1 = ''.join(fin)
fin_2 = list(fin_1)
print(fin_1, len(fin_1))
print(len(fin_2))

for i in range(len(fin)):
	if len(fin[i]) < 8:
		print(fin[i])
		'''
msg = 'bc35dcc9982c88a788f6feeb177cae1143695d9f4e6bad70d8400e63f91f23610666a49b7d4fbd8925444109a54e11744dc859acd20fa4cf212e5146d5d26f91d477e8da0d848075ff875dca2e410e0e9bd912cefbcc1b3e0c7bec86e7f2b81390b23cf563c2a2d77f2f7f826681366be2138a820fec323fcc9e83be19ccfe23'
msg1 = '32,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,74,65,73,74,2E,6A,69,6E,77,6F,6F,73,69,2E,63,6F,2E,6B,72,20,38,32,32,31,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,2F,49,47,57,2E,65,78,65,20,20,20,20,66,74,70,73,30,31,20,20,20,20,66,74,70,73,30,31'
msg2 = msg1.replace(',','')

msg_list = []
dec_list = []
fin_list = []


msg_list2 = []
dec_list2 = []
fin_list2 = []
msg_list = []
dec_list = []
fin_list = []

for i in range(int((len(msg))/2)) :
    msg_list.append((msg[2*i:2*i+2]))
for i in range(len(msg_list)):
	dec_list.append(int(msg_list[i],16))
for i in range(len(dec_list)):
	fin_list.append(hex(int(msg_list[i],16)))

print(hex(188), type(int(hex(188),16)))

print("finlist:",msg_list)
print(type(fin_list[1]))

intlist = []
for i in range(len(msg_list)):
	intlist.append(int(msg_list[i],16))
print(intlist)
'''
msg1 = '32,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,74,65,73,74,2E,6A,69,6E,77,6F,6F,73,69,2E,63,6F,2E,6B,72,20,38,32,32,31,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,2F,49,47,57,2E,65,78,65,20,20,20,20,66,74,70,73,30,31,20,20,20,20,66,74,70,73,30,31'
msg2 = msg1.replace(',','')

for i in range(int((len(msg2))/2)) :
    msg_list2.append(('0x'+msg2[2*i:2*i+2]))
for i in range(len(msg_list2)):
	dec_list2.append(int(msg_list2[i],16))
for i in range(len(dec_list2)):
	fin_list2.append(hex(int(msg_list2[i],16)))

print(fin_list2)
# msg_list > hex_string

#an_ integer > int(msg_list[i], 16)

# hex_value = hex(an_integer) > fin_list.append(hex(int(msg_list[i],16)))

print( len(fin_list), len(fin_list2))
'''