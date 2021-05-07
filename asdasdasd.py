import hashlib, os, socket, threading, time, datetime, binascii, asyncio, sys
from multiprocessing import Queue
#from db.database import Database
#from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
from crccheck.crc import Crc, Crc16Ccitt
#from paramiko.sftp_client import SFTP
import distributed
from dateutil.parser import parse
from ctypes import *

host = "192.168.1.203"
port = 8000
SEED = CDLL('/root/sensor/seed128/KISA_SEED_CBC.so')
pbszUserKey = ('0x88,0xE3,0x4F,0x8F,0x08,0x17,0x79,0xF1,0xE9,0xF3,0x94,0x37,0x0A,0xD4,0x05,0x89')
pbszIV = ('0x26,0x8D,0x66,0xA7,0x35,0xA8,0x1A,0x81,0x6F,0xBA,0xD9,0xFA,0x36,0x16,0x25,0x01')
pbszPlainText = '3131313130303030'

encpt = SEED.SEED_CBC_Encrypt(pbszUserKey, pbszIV, pbszPlainText, len(pbszPlainText))
print("encrypt :", encpt)
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
                    print("sftp message :", read_data[36:])
                    device_upgrade_handler.sftp_download(read_data[36:])
                
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
'''
class send_recv: # 송수신메세지 처리 클래스. 
    raw_data = q.get()
    
    #NEED SEED128 DECODE
    def return_order() :
        data_list = []
        for i in range(0, len(send_recv.raw_data),+2):
            data_list.append(send_recv.raw_data[i:i+2])
        return data_list[0:4]

    def def_msg():
        order_c = send_recv.raw_data[0:8]
        if order_c == '54555047' : #TUPG's ascii : \x54\x55\x50\x47
            send_msg = msg_handler.TUPG()
            return send_msg

        elif order_c == '50555047': #PUPG's ascii
            upgrade_msg = send_recv.raw_data[36:]
            #device_upgrade_handler.sftp_download(upgrade_msg)
print("4")'''
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
        msgd = []
        print('duh message:', msg)
            
        
    
        tp = msg[0:2]
        dl_host = msg[2:83]
        dl_port = msg[83:93]
        print(tp,dl_host,dl_port)
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
            #message.extend(b'\x02')	#stx
            #message.extend(':'.encode("ASCII"))
            
            message.extend(order[].encode("ASCII")) #메세지명
            message.extend(data.S_SITE_ID.encode("ASCII"))	#사업장7자리+굴뚝3자리
            message.extend(data.DATE.encode("ASCII"))	##전체길이
            message.extend(data.S_DEVICE30_YN.encode("ASCII"))	##버전
            message.extend(data.S_DEVICE31_CD.encode("ASCII"))	##해쉬코드
            message.extend(data.S_DEVICE31_YN.encode("ASCII"))	##테일러

            message.extend('Tpm2+NPl/SYPq84leQ3MwVcSLl435284R+E6vZlYFDE=<EOF>'.encode("ASCII"))	#etx
            #message.extend('\x03'.encode("ASCII"))	#etx


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
