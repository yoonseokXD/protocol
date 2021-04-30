import hashlib, paramiko
import os
import socket, threading, time, binascii
from multiprocessing import Queue
#from db.database import Database
#from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
import binascii, asyncio
from crccheck.crc import Crc, Crc16Ccitt
from paramiko.sftp_client import SFTP



host = "192.168.1.203"
port = 90

q = Queue()
order = ['TDAT', #0.측정데이터자료전송                  Gateway -> Server 
		 'PDUM', #1.저장자료 요청                          Server -> Gateway
		 'TDUM', #2.저장자료요청 응답                   Gateway -> Server
		 'TFDT', #3.미전송자료 자동전송                 Gateway -> Server
		 'PSEP', #4.비밀번호 암호변경지시                  Server -> Gateway
		 'TVER', #5.기동정보전송                        Gateway -> server
		 'PTIM', #6.기동정보메세지 수신시 서버시간 전송     Server -> Gateway
		 'PUPG', #7.업그레이드지시전송                      Server -> Gateway
		 'TUPG', #8.업그레이드결과전송                   Gateway -> Server
		 'TCNG', #9.설정값 변경항목 자동 전송            Gateway -> Server
		 'PVER', #10.버전정보 조회요청                      Server -> Gateway
		 'DVER', #11.버전정보 조회응답                   Gateway -> Server
		 'PSET'] #12.수동 시간 설정                         Server -> Gateway


"""
# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = ''
# 서버에서 지정해 놓은 포트 번호입니다.
PORT = 3030


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다.
client_socket.connect((HOST, PORT))



sql = '''
         SELECT S_SITE_ID as CODE  from T_DEVICE
        '''

db_session = Database.getSession()"""

db_datas = ('1100001001').encode('ascii')




class asyncio_client():

    async def run_client():
        reader : asyncio.StreamReader
        writer : asyncio.StreamReader
        reader, writer = await asyncio.open_connection(host,port)
        print("connection info :",host,':',port)

        
        while True :
            data = send_handler.upgrade_result_send() #NEED SEED128 ENCODE
            if not data :
                break
            payload = data
            writer.write(payload)
            await writer.drain()
            print(("sent : {} bytes.\n").format(len(payload)))
            read_data = await reader.read(1024)
            print(("received : {} bytes").format(len(read_data)))
            if read_data == '06': #ACK부분 수정필요. 수신데이터와 분리할 필요가 있음
                break
            elif read_data == '15' :
                pass
            elif read_data == '04' :
                pass
            else :
                q.put(read_data)
                print(("message : {}").format(read_data.decode()))
                writer.close()
                await writer.wait_close()
                
        print("closing connection")
        writer.close()
        await writer.wait_closed()

class data_handler: # 수신메세지 분석 클래스. 
    raw_data = q.get()
    #NEED SEED128 DECODE

    pass


class send_handler:
    def __init__(self):
        self.db_datas = db_datas

    def CRC16_CCITT(hd, bd):
        data = hd+bd
        crc16 = Crc16Ccitt.calc(data)
        return crc16

    def SHA_256():
        with open('/root/sensor/main.py', 'rb') as crypt :
            s = crypt.read()
            sha_key = hashlib.sha256(s).hexdigest().upper()
        return sha_key

    def version_info():
        pass
    
    def upgrade_result_send(): #TUPG
        msg = bytearray()
        msg_type = order[8].encode('ascii')
        client_version = ('2.03').encode('ascii')
        hash_code = bytes(send_handler.SHA_256())
        CRC_len = 2
        msg_len = (('{}').format(len(msg_type)+len(db_datas)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii')
        
        CRC_code = hex(send_handler.CRC16_CCITT(msg_type+db_datas+msg_len, client_version+hash_code)).replace('0x','').upper()
        print(CRC_code, type(CRC_code))
        msg.extend(msg_type)
        msg.extend(db_datas)
        msg.extend(msg_len)
        msg.extend(client_version)
        msg.extend(hash_code)
        msg.extend(CRC_code.encode('ascii'))
        print(msg)
        return msg

    def send_message():
        pass
class device_upgrade_handler :
    def sftp_download():
        host = 
        port =
        serverpath = 
        id = 
        pwd = 
        clientpath = '/root/sensor/updatePakage'
        filename =
        transport = paramiko.Transport(host,port)
        transport.connect(username=id, password=pwd)
        SFTP.get(serverpath, clientpath)
        SFTP.close()
        transport.close()
    def upgrade():
        os.system("chmod 755 /root/sensor/updatePakage/update.sh")
        os.system("/root/sensor/updatePakage/update.sh")
    
    pass


















if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio_client.run_client())



































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