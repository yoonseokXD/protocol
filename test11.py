import hashlib, os, socket, threading, time, datetime, binascii, asyncio, sys
from multiprocessing import Queue
#from db.database import Database
#from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
from crccheck.crc import Crc, Crc16Ccitt
#from paramiko.sftp_client import SFTP
import distributed
from dateutil.parser import parse
import ctypes, pysftp
from array import *
import numpy as np
import struct

host = "192.168.1.203"
port = 8000




kisa_seed_cbc = ctypes.cdll.LoadLibrary("./kisa_seed_cbc.so")

q = Queue()
tq = Queue()

order = ['TDAT', #0.측정데이터자료전송                  Gateway -> Server           정기실행
         'PDUM', #1.저장자료 요청                          Server -> Gateway
         'TDUM', #2.저장자료요청 응답                   Gateway -> Server           요청필요
         'TFDT', #3.미전송자료 자동전송                 Gateway -> Server           정기실행
         'PSEP', #4.비밀번호 암호변경지시                  Server -> Gateway
         'TVER', #5.기동정보전송                        Gateway -> server           정기실행
         'PTIM', #6.기동정보메세지 수신시 서버시간 전송     Server -> Gateway
         'PUPG', #7.업그레이드지시전송                      Server -> Gateway
         'TUPG', #8.업그레이드결과전송                   Gateway -> Server          요청필요
         'TCNG', #9.설정값 변경항목 자동 전송            Gateway -> Server          정기실행
         'PVER', #10.버전정보 조회요청                      Server -> Gateway
         'DVER', #11.버전정보 조회응답                   Gateway -> Server          요청필요
         'PSET'] #12.수동 시간 설정                         Server -> Gateway

# 0 3 5 정기실행
# 수신 후 device 설정 : 6, 8, 12
# 1>2 , 4>9, 7>8, 10>11 요청처리

"""
sql = '''
         SELECT S_SITE_ID as CODE  from T_DEVICE
        '''

db_session = Database.getSession()"""


db_datas = ('1100001001').encode('ascii')
JEJO_CODE = 'HR'.encode('ascii')

class CBC():
    pbszUserKey = [0x0E9, 0x0F3, 0x094, 0x037, 0x00A, 0x0D4, 0x005, 0x089, 0x088, 0x0E3, 0x04F, 0x08F, 0x008, 0x017, 0x079, 0x0F1]
    pbszIV = [0x06F, 0x0BA, 0x0D9, 0x0FA, 0x036, 0x016, 0x025, 0x001, 0x026, 0x08D, 0x066, 0x0A7, 0x035, 0x0A8, 0x01A, 0x081]
    plainText = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F,
             0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
    pbszCipherText = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
                  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]


    pbszUserKey_array = (ctypes.c_ubyte * len(pbszUserKey))(*pbszUserKey)
    pbszIV_array = (ctypes.c_ubyte * len(pbszIV))(*pbszIV)
    plainText_array1 = (ctypes.c_ubyte * len(plainText))(*plainText)
    plainText_array = (ctypes.c_ubyte * len(plainText))(*plainText)
    pbszCipherText_array = (ctypes.c_ubyte * len(pbszCipherText))(*pbszCipherText)

    kisa_seed_cbc = ctypes.cdll.LoadLibrary("./kisa_seed_cbc.so")
    seed_cbc_encrypt = kisa_seed_cbc.SEED_CBC_Encrypt
    seed_cbc_decrypt = kisa_seed_cbc.SEED_CBC_Decrypt

	#샘플 문장. 전체 평문의 길이를 계산하기 위한 용도로 사용한다
    ipAddr = "test.jinwoosi.co.kr"
    portNum = "8282"
    pathName = "/IGW.exe"
    loginId = "ftps01"
    loginPw = "ftps01"
    PUPG_msg = "2%40s%5s%50s%10s%10s" %(ipAddr, portNum, pathName, loginId, loginPw)
    bPUPG_msg = bytes(PUPG_msg, 'utf-8')
    PUPG_array = (ctypes.c_ubyte * len(bPUPG_msg))(*bPUPG_msg)
    
#seed_cbc_encrypt(pbszUserKey_array, pbszIV_array, plainText_array, pbszCipherText_array)

    def encrypt(msg) : #인풋 메세지 암호화 함수
        global res_e
        res_e = CBC.seed_cbc_encrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, CBC.plainText_array, len(CBC.PUPG_msg), CBC.pbszCipherText_array) # key, IV, 평문, 평문 길이, 암호문출력버퍼
        print("encrypt res :", res_e)

        range(0, res_e)
        for i in range(res_e):
                print(hex(int(CBC.pbszCipherText_array[i])), end=' ')
        print("\r\n")

    def encrypt_sample() : # decrypt 함수의 암호문 길이를 리턴하기 위한 함수이다.
        
        res = CBC.seed_cbc_encrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, CBC.plainText_array, len(CBC.PUPG_msg), CBC.pbszCipherText_array) # key, IV, 평문, 평문 길이, 암호문출력버퍼
        print("encrypt res :", res)

        range(0, res)
        for i in range(res):
                print(hex(int(CBC.pbszCipherText_array[i])), end=' ')
        return res

    def decrypt(msg) :
        print("msg:", msg)
        inputEncryptedStr = msg
        print("inputEncryptedStr:", inputEncryptedStr)
        inputEncryptedStr_list = []
        print("inputEncryptedStr_list:", inputEncryptedStr_list)
        for i in range(int((len(inputEncryptedStr))/2)) :
            inputEncryptedStr_list.append((inputEncryptedStr[2*i:2*i+2]))
        print("inputEncryptedStr_list2:", inputEncryptedStr_list)
        intlist = []
        for i in range(len(inputEncryptedStr_list)):
            intlist.append(int(inputEncryptedStr_list[i],16))
        print("intlist:", intlist)
        input_array = (ctypes.c_ubyte * len(intlist))(*intlist)

        res_d = CBC.seed_cbc_decrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, input_array, CBC.encrypt_sample(), CBC.plainText_array) # key, IV, 암호문, 암호문 길이, 평문출력버퍼

        decrypt_result = ''
        print("decrypt res :", res_d)
        range(0, res_d)
        for i in range(res_d):
                print(hex(CBC.plainText_array[i]), end=' ')
                decrypt_result+=chr(CBC.plainText_array[i])
                
        print("\r\n")
        print("Dectypted Result:",decrypt_result)
        return decrypt_result


'''
    ######################################################################################################
    res_e = seed_cbc_encrypt(pbszUserKey_array, pbszIV_array, plainText_array, 63, pbszCipherText_array) # key, IV, 평문, 평문 길이, 암호문출력버퍼
    print("encrypt res :", res_e)

    range(0, res_e)
    for i in range(res_e):
            print(hex(int(pbszCipherText_array[i])), end=' ')
    print("\r\n")
    ######################################################################################################
    res_d = seed_cbc_decrypt(pbszUserKey_array, pbszIV_array, pbszCipherText_array, res_e, plainText_array) # key, IV, 암호문, 암호문 길이, 평문출력버퍼
    print("decrypt res :", res_d)
    range(0, res_d)
    for i in range(res_d):
            print(hex(plainText_array[i]), end=' ')
    for i in range(res_d):
            print(chr(plainText_array[i]), end='')
    print("\r\n")
'''

class asyncio_client():
        
    async def run_client():
        
        reader, writer = await asyncio.open_connection(host,port)
        print("connection info :",host,':',port)
        writer.write(msg_handler.TVER())
        
        while True :
            
            data = msg_handler.TVER() #NEED SEED128 ENCODE
            if not data :
                break
            payload = data
            payload_nak = b'15'
            
            
            read_data = await reader.read(1024)
            print("---- async protocol start ----")
            print(("received : {} bytes").format(len(read_data)))
            if read_data == b'06': #ACK부분 수정필요. 수신데이터와 분리할 필요가 있음
                try :
                    print("ack")
                    pass
                except : 
                    pass

            #NAK
            elif read_data == b'15' :
                try:
                    nak_order = q.get()
                    print(nak_order)
                    print("nak")
                    if nak_order == '54564552' :
                        print("ORDER : TVER")
                        
                        payload = msg_handler.TVER()
                        writer.write(payload)
                        writer.write(payload)
                    
                    elif nak_order == '54555047' :
                        print("ORDER : TUPG")
                        payload = msg_handler.TUPG()
                        print(payload)
                        writer.write(payload)
                        writer.write(payload)
                    elif nak_order == '50555047' :
                        print("order : PUPG")
                except :
                    print("queue is empty")
                    pass

            #EOT
            elif read_data == b'04' :
                print("etc")
                pass

            #start

            else :
                order = read_data[0:8].decode('ascii')
                q.put(order)
                if order == '54564552' : #TVER
                    print("ORDER : TVER")
                    
                    payload = msg_handler.TVER()
                    writer.write(payload)
                    
                elif order == '54555047' : #TUPG
                    print("ORDER : TUPG")
                    payload = msg_handler.TUPG()
                    print(payload)
                    writer.write(payload)
                    
                elif order == '50555047' : #PUPG업그레이드지시전송, 결과는 TUPG
                    print("order : PUPG")
                    print("sftp message :", read_data[36:(len(read_data)-4)])
                    device_upgrade_handler.sftp_download(read_data[36:(len(read_data)-4)])
                
                elif order == '50534554' : # PSET
                    if len(read_data) != 64 :
                        writer.write(payload_nak)
                    else :
                        payload = b'06'
                        writer.write(payload)
                        tq.put(read_data[18:29])
                        msg_handler.PSET()

                elif order == '50564552' : #PVER
                    if len(read_data) != 40 :
                        writer.write(payload_nak)
                    else :
                        payload = msg_handler.DVER()
                        writer.write(payload)
                else : 
                    pass
            print(("sent : {} bytes.").format(len(payload)))
            print(("message : {}, {}").format(read_data.decode(), type(read_data.decode())))
                

        print("closing connection")
        writer.close()
        await writer.wait_closed()

        
class msg_handler:

    def CRC16_CCITT(hd, bd):
        data = hd+bd
        crc16 = Crc16Ccitt.calc(data)
        return crc16

    def SHA_256():
        with open('/root/sensor/main.py', 'rb') as crypt :
            s = crypt.read()
            sha_key = hashlib.sha256(s).hexdigest().upper().encode('ascii')
        return sha_key

    def version_info():
        pass

    def TCNG():
        # 바디에 측정값이 필요
        pass
    def TVER():
        msg = bytearray()
        msg_type = order[5].encode('ascii')
        id_code = db_datas
        maker_code = JEJO_CODE
        hash_code = bytes(msg_handler.SHA_256())
        client_version = ('2.03').encode('ascii')
        CRC_len = 2
        
        msg_len = (('{}').format(len(msg_type)+len(id_code)+len(maker_code)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii') #전체메세지길이
        CRC_code = hex(msg_handler.CRC16_CCITT(msg_type+id_code+msg_len, maker_code+hash_code+client_version)).replace('0x','').upper()
        msg.extend(msg_type)
        msg.extend(id_code)
        msg.extend(msg_len)
        msg.extend(maker_code)
        msg.extend(hash_code)
        msg.extend(client_version)
        msg.extend(CRC_code.encode('ascii'))
        return msg

    def DVER():
        msg = bytearray()
        msg_type = order[11].encode('ascii')
        id_code = db_datas
        maker_code = JEJO_CODE
        hash_code = bytes(msg_handler.SHA_256())
        client_version = ('2.03').encode('ascii')
        CRC_len = 2
        
        msg_len = (('{}').format(len(msg_type)+len(id_code)+len(maker_code)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii') #전체메세지길이
        CRC_code = hex(msg_handler.CRC16_CCITT(msg_type+id_code+msg_len, maker_code+hash_code+client_version)).replace('0x','').upper()
        msg.extend(msg_type)
        msg.extend(id_code)
        msg.extend(msg_len)
        msg.extend(maker_code)
        msg.extend(hash_code)
        msg.extend(client_version)
        msg.extend(CRC_code.encode('ascii'))
        return msg

    def TUPG(): #TUPG
        msg = bytearray()      
        msg_type = order[8].encode('ascii') #전역변수 order 참조
        id_code = db_datas
        client_version = ('2.03').encode('ascii') #메인 실행 프로그램으로부터 버전정보를 받아와야함.
        hash_code = bytes(msg_handler.SHA_256()) #메인 실행 프로그램을 해쉬화 해야함.
        CRC_len = 2
        msg_len = (('{}').format(len(msg_type)+len(id_code)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii') #전체메세지길이
        
        CRC_code = hex(msg_handler.CRC16_CCITT(msg_type+id_code+msg_len, client_version+hash_code)).replace('0x','').upper() #오류검정코드
        print("msghandler :",CRC_code, type(CRC_code))
        msg.extend(msg_type)
        msg.extend(db_datas)
        msg.extend(msg_len)
        msg.extend(client_version)
        msg.extend(hash_code)
        msg.extend(CRC_code.encode('ascii'))
        return msg
    def PSET():
        time_string = tq.put()
        ts = '20'+time_string
        z = str("'"+ts[0:4]+'-'+ts[4:6]+'-'+ts[6:8]+' '+ts[8:10]+':'+ts[10:12]+':'+'00'+"'")
        os.system("date -s" + z)

class device_upgrade_handler :
    def sftp_download(msg):
        dcd_msg = msg.decode()
        decrypt_msg = CBC.decrypt(dcd_msg)
        print('duh message:', decrypt_msg)
        
        
    
        tp = decrypt_msg[0:2]
        dl_host = decrypt_msg[2:42].replace(' ','')
        dl_port = decrypt_msg[42:46].replace(' ','')
        dl_path = decrypt_msg[46:96].replace(' ','')
        dl_id = decrypt_msg[96:106].replace(' ','')
        dl_pw = decrypt_msg[106:116].replace(' ','')
        print("type:",tp)
        print("host:",dl_host)
        print("port:",dl_port)
        print("path:",dl_path)
        print("id:",dl_id)
        print("pw:",dl_pw)
        dl_sftp =  pysftp.Connection(dl_hos,username='dl_id', password='dl_pw')
        dl_sftp.get(dl_path, '/root/sensor/Gupdatepkg')
        dl_sftp.close()
        '''
        serverpath = 
        id = 
        pwd = 
        clientpath = '/root/sensor/updatePakage'
        filename =
        
        transport = paramiko.Transport(dl_host,dl_port)
        transport.connect(username=id, password=pwd)
        SFTP.get(serverpath, clientpath)
        SFTP.close()
        transport.close()
        device_upgrade_handler.upgrade()
        
    def upgrade():
        os.system("rm -rf /root/sensor/updatePakage")
        #압축풀기 들어가야함.
        os.system("chmod 755 /root/sensor/updatePakage/update.sh")
        os.system("/root/sensor/updatePakage/update.sh")
    


'''








if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(asyncio_client.run_client())
    else:
        print('Starting new event loop')
        loop.run_until_complete(asyncio_client.run_client())
    print(msg_handler.TUPG())
































'''
while(True):

        
        
        #result = {}
        for data in db_datas:
            #result[data.ID_AD_NUM, data.S_DEVICE01_ID] = [data.S_DEVICE1_VALUE, data.S_MEASURE_DATE]

    #db_data = db_session.query(TDEVICEDATA5SEC).filter(TDEVICEDATA5SEC.ID_DEVICE_DATA_5SEC == max_id).limit(1)

        #if(db_datas.count() > 0):

            #data = db_datas

        
            # 메시지를 생성합니다.
            message = bytearray()
            #message.extend(b'\x02')    #stx
            #message.extend(':'.encode("ASCII"))
            
            message.extend(order[].encode("ASCII")) #메세지명
            message.extend(data.S_SITE_ID.encode("ASCII"))    #사업장7자리+굴뚝3자리
            message.extend(data.DATE.encode("ASCII"))    ##전체길이
            message.extend(data.S_DEVICE30_YN.encode("ASCII"))    ##버전
            message.extend(data.S_DEVICE31_CD.encode("ASCII"))    ##해쉬코드
            message.extend(data.S_DEVICE31_YN.encode("ASCII"))    ##테일러

            message.extend('Tpm2+NPl/SYPq84leQ3MwVcSLl435284R+E6vZlYFDE=<EOF>'.encode("ASCII"))    #etx
            #message.extend('\x03'.encode("ASCII"))    #etx


            print(message)
            

            # 메시지를 전송합니다.
            print("메시지 전송")
            
            client_socket.send(message)
            
            
        break
            

                
        
        # 메시지를 수신합니다.
        db_datas = client_socket.recv(1024)
        print('Received', repr(db_datas.decode()))

    

    #

# 소켓을 닫습니다.
client_socket.close()



'''
