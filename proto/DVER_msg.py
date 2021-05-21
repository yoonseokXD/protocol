from array import *
import ctypes
import socket
import hashlib
import binascii

HOST = '10.101.151.158'
#HOST = '192.168.219.104'
HOST_PORT = 5010
LOCAL_PORT = 9090

clib_sha = ctypes.cdll.LoadLibrary("./kisa_sha256.so")
clib_crc = ctypes.cdll.LoadLibrary("./crc16ccitt.so")

msgName = "DVER"
siteCode = "1100176"
preventCode = "001"
manufacCode = "WB"
msgLength = 58
verNumber = "1.01"

headerMsg = "%4s%7s%3s%4d" %(msgName, siteCode, preventCode, msgLength)
print("\r\n")
print('headerMsg len=', len(headerMsg))
print('headerMsg:', headerMsg)
encodedString = headerMsg.encode()
headerMsgArray = bytearray(encodedString)

sha256InputData = (ctypes.c_ubyte * len(headerMsgArray))(*headerMsgArray)
encResult = bytearray(32)
encResult_c = (ctypes.c_ubyte * len(encResult))(*encResult)
clib_sha.SHA256_Encrpyt(sha256InputData, len(headerMsg), encResult_c)
print('encResult_c', end='=')
print(''.join('{:02x}'.format(x) for x in encResult_c))
#range(0, 32)
#for i in range(32):
#    print(hex(encResult_c[i]), end=' ')
print("\r\n")

encodedString = headerMsg.encode()
sendMsg = bytearray(encodedString)
encodedString = manufacCode.encode()
sendMsg += bytearray(encodedString)
sendMsg += encResult_c
encodedString = verNumber.encode()
sendMsg += bytearray(encodedString)

crcInputData = (ctypes.c_ubyte * len(sendMsg))(*sendMsg)
crc16value = clib_crc.crc16_ccitt(crcInputData, len(sendMsg))
print('crc16value', end='=')
print(hex(crc16value))
sendMsg += crc16value.to_bytes(2, byteorder="big")

print('sendMsg len=', len(sendMsg))
print('sendMsg', end='=')
print(sendMsg)
print('sendMsg', end='=')
print(''.join('{:02x}'.format(x) for x in sendMsg))
print("\r\n")

sdmsg = bytes()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, HOST_PORT))
sendLen = client_socket.send(sendMsg)
print('sendLen=', sendLen)
client_socket.close()

