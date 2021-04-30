import sys, queue
from collections import deque

key = [0xE9,0xF3,0x94,0x37,0x0A,0xD4,0x05,0x89,0x88,0xE3,0x4F,0x8F,0x08,0x17,0x79,0xF1]
key_b = []
key_b2 = []
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

'''
if len(key_b2[i]) < 8 :
		for i in range(0, (len(key_b2)-1),+1):
			if len(key_b2[i]) < 8 :
				deq.appendleft(0)
'''

fin = ['11101001', '11110011', '10010100', '00110111', '00001010', '11010100', '00000101', '10001001', '10001000', '11100011', '01001111', '10001111', '00001000', '00010111', '01111001', '11110001']
fin_1 = ''.join(fin)
fin_2 = list(fin_1)
print(fin_1, len(fin_1))
print(len(fin_2))

for i in range(len(fin)):
	if len(fin[i]) < 8:
		print(fin[i])