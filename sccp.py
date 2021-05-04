import hashlib, paramiko
import os
import socket, threading, time, binascii
from multiprocessing import Queue
#from db.database import Database
#from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
import binascii, asyncio
from crccheck.crc import Crc, Crc16Ccitt
from paramiko.sftp_client import SFTP

host = "localhost"
port = 8000

q = Queue()

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


"""
sql = '''
         SELECT S_SITE_ID as CODE  from T_DEVICE
        '''

db_session = Database.getSession()"""
print("3")

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

            
            
            read_data = await reader.read(1024)
            print("---- async protocol start ----")
            print(("received : {} bytes").format(len(read_data)))
            if read_data == b'06': #ACK부분 수정필요. 수신데이터와 분리할 필요가 있음
                print("ack")
                pass
            elif read_data == b'15' :
                print("nak")
                pass
            elif read_data == b'04' :
                print("etc")
                pass
            else :
                order = read_data[0:8].decode('ascii')
                if order == '54564552' :
                    print("ORDER : TVER")
                    
                    super(payload) = msg_handler.TVER()
                    writer.write(payload)
                    
                elif order == '54555047' :
                    print("ORDER : TUPG")
                    payload = msg_handler.TUPG()
                    print(payload)
                    writer.write(payload)
                    
                elif order == '50555047' :
                    print("order : PUPG")
                    
                    
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
        with open('C:\Python\diko\makingbot.py', 'rb') as crypt :
            s = crypt.read()
            sha_key = hashlib.sha256(s).hexdigest().upper().encode('ascii')
        return sha_key

    def version_info():
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
'''
class device_upgrade_handler :
    def sftp_download(msg):
        msgd = []
        print('duh message:', msg)
        for i in range(len(msg)):
            msgd.append(chr(str(msg[i:i+2])))
        print(msgd)
        
    
        tp = msg[0:2]
        dl_host = msg[2:83]
        dl_port = msg[83:93]
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
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(asyncio_client.run_client())
    else:
        print('Starting new event loop')
        asyncio.run(asyncio_client.run_client())
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