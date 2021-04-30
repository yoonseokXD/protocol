import socket, threading, time, binascii
from multiprocessing import Queue
#from db.database import Database
#from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
import binascii, asyncio
from crccheck.crc import Crc, Crc16Ccitt



host = "192.168.1.203"
port = 90

q = Queue()
order = ['TDAT', #0.측정데이터전송\자료전송 G>S
		 'PDUM', #1.저장자료요청/전송\요청 S>G
		 'TDUM', #2.저장자료요청/전송\응답
		 'TFDT', #3.미전송자료 전송\자동전송
		 'PSEP', #4.비밀번호변경 전송\암호변경지시
		 'TVER', #5.
		 'PTIM', #6.
		 'PUPG', #7.
		 'TUPG', #8.
		 'TCNG', #9.
		 'PVER', #10.
		 'DVER', #11.
		 'PSET'] #12.


"""
# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '218.146.19.3'
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
        print("connection info :", host,':',port)
        while True :
            data = protocol_client_send.upgrade_result_send()
            if not data :
                break
            payload = data
            writer.write(payload)
            await writer.drain()
            print(("sent : {} bytes.\n").format(len(payload)))
            read_data = await reader.read(1024)
            print(("received : {} bytes").format(len(read_data)))
            print(("message : {}").format(read_data.decode()))
        print("closing connection")
        writer.close()
        await writer.wait_closed()




class protocol_client_send:
    def __init__(self):
        self.db_datas = db_datas

    def CRC16_CCITT(hd, bd):
        data = hd+bd
        crc16 = Crc16Ccitt.calc(data)
        return crc16

    def upgrade_result_send():
        msg = bytearray()
        msg_type = order[8].encode('ascii')
        client_version = ('2.03').encode('ascii')
        hash_code = (b'0547501027887948D5BB3912933B09476D69F434E260F96ACA3A60829877C6DD78B0')
        CRC_len = 2
        msg_len = (('{}').format(len(msg_type)+len(db_datas)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii')
        
        CRC_code = hex(protocol_client_send.CRC16_CCITT(msg_type+db_datas+msg_len, client_version+hash_code)).replace('0x','').upper()
        print(CRC_code, type(CRC_code))
        msg.extend(msg_type)
        msg.extend(db_datas)
        msg.extend(msg_len)
        msg.extend(client_version)
        msg.extend(hash_code)
        msg.extend(CRC_code.encode('ascii'))
        print(msg)
        return msg
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