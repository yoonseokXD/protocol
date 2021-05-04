import binascii
str = b'5054494D313130303030313030312020333232303037303930303030303204F7'




lst = []
for i in range(int(len(str)/2)):
	lst.append(str[2*i:2*i+2])


asd = binascii.unhexlify(str)
print(asd)


dct = {1:'a', 2:'b'}

print(dct[1])