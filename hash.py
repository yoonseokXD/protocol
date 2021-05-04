import hashlib, sys
from collections import deque

q = deque()

f = open("socket_client.py", 'rb')
data = f.read()
f.close()

print("sha256:", hashlib.sha256(data).hexdigest().upper())
bsr = b'\x54\x55\x50\x47'
sr = '54555047'
sr.encode('ascii')
list1 = []
list2 = []
print(sr[0:2])

for i in range (0, len(sr),+2):
	list1.append(sr[i:i+2])
print(list1)
print(bsr.decode('ascii'))
for i in range(len(list1)) :
	list2.append(('\\'+'x'+list1[i]))
	for i in range(len(list2)):
		list2[i] = q.popleft(list2[i])
	
print(list2)