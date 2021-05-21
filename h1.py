import binascii, time, datetime
import codecs
from dateutil.parser import parse
strng= b'bc35dcc9982c88a788f6feeb177cae1143695d9f4e6bad70d8400e63f91f23610666a49b7d4fbd8925444109a54e11744dc859acd20fa4cf212e5146d5d26f91d477e8da0d848075ff875dca2e410e0e9bd912cefbcc1b3e0c7bec86e7f2b81390b23cf563c2a2d77f2f7f826681366be2138a820fec323fcc9e83be19ccfe235AEE505550473131303030303130303120313438bc35dcc9982c88a788f6feeb177cae1143695d9f4e6bad70d8400e63f91f23610666a49b7d4fbd8925444109a54e11744dc859acd20fa4cf212e5146d5d26f91d477e8da0d848075ff875dca2e410e0e9bd912cefbcc1b3e0c7bec86e7f2b81390b23cf563c2a2d77f2f7f826681366be2138a820fec323fcc9e83be19ccfe23'.decode()


__version__ = '1.0'

lst = []
for i in range(int(len(strng)/2)):
	lst.append(strng[2*i:2*i+2])


asd = binascii.unhexlify(strng)
print(asd)


dct = {1:'a', 2:'b'}

print(dct[1])

y = '20'+"200709232300"
z = str("'"+y[0:4]+'-'+y[4:6]+'-'+y[6:8]+' '+y[8:10]+':'+y[10:12]+':'+'00'+"'")
#z = datetime.datetime.strptime(y, "%y-%m-%d %H:%M:00" )
print(z)
dt = parse(z)
print(dt, type(dt))


ln = b'5053455431313030303031303031202033323230303730393233323330305929'

print (len(ln))

print(__version__)


hexdcd = binascii.unhexlify(strng)
print('hexdcd :', hexdcd)

decode_hex = codecs.getdecoder("hex_codec")

lst = []
'''
for i in range(len(strng)):
	lst.append(chr[strng[i:i+2]])
	
print(lst)'''

print(ord(strng[0:1]))

def __bootstrap__():
        global __bootstrap__, __loader__, __file__
        import sys, pkg_resources, imp
        __file__ = pkg_resources.resource_filename(__name__,'kisa_seed_cbc.so')
        __loader__ = None; del __bootstrap__, __loader__
        imp.load_dynamic(__name__,__file__)
    __bootstrap__()
