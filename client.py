import socket, time
from db.database import Database
from db.models import TDEVICEDATA5MINSERVER, TDEVICEDATA1MINSERVER
import binascii


# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '218.146.19.3'
# 서버에서 지정해 놓은 포트 번호입니다.
PORT = 3030


# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다.
client_socket.connect((HOST, PORT))

db_session = Database.getSession()


while(True):

        
        sql = '''
         SELECT
            AA.GW_ID,AA.DATE,AA.S_SITE_ID,AA.S_PREVENT_CD,AA.S_DEVICE01_CD,AA.S_DEVICE01_YN,AA.S_DEVICE02_CD,AA.S_DEVICE02_YN,AA.S_DEVICE03_CD,AA.S_DEVICE03_YN,AA.S_DEVICE04_CD,AA.S_DEVICE04_YN,AA.S_DEVICE05_CD,AA.S_DEVICE05_YN,
            AA.S_DEVICE06_CD,AA.S_DEVICE06_YN,AA.S_DEVICE07_CD,AA.S_DEVICE07_YN,AA.S_DEVICE08_CD,AA.S_DEVICE08_YN,AA.S_DEVICE09_CD,AA.S_DEVICE09_YN,AA.S_DEVICE10_CD,AA.S_DEVICE10_YN,
            AA.S_DEVICE11_CD,AA.S_DEVICE11_YN,AA.S_DEVICE12_CD,AA.S_DEVICE12_YN,AA.S_DEVICE13_CD,AA.S_DEVICE13_YN,AA.S_DEVICE14_CD,AA.S_DEVICE14_YN,AA.S_DEVICE15_CD,AA.S_DEVICE15_YN,AA.S_DEVICE16_CD,AA.S_DEVICE16_YN,
            BB.S_DEVICE01_CD AS S_DEVICE17_CD,BB.S_DEVICE01_YN AS S_DEVICE17_YN,BB.S_DEVICE02_CD AS S_DEVICE18_CD,BB.S_DEVICE02_YN AS S_DEVICE18_YN,BB.S_DEVICE03_CD AS S_DEVICE19_CD,BB.S_DEVICE03_YN AS S_DEVICE19_YN,BB.S_DEVICE04_CD AS S_DEVICE20_CD,BB.S_DEVICE04_YN AS S_DEVICE20_YN,BB.S_DEVICE05_CD AS S_DEVICE21_CD,BB.S_DEVICE05_YN AS S_DEVICE21_YN,
            BB.S_DEVICE06_CD AS S_DEVICE22_CD,BB.S_DEVICE06_YN AS S_DEVICE22_YN,BB.S_DEVICE07_CD AS S_DEVICE23_CD,BB.S_DEVICE07_YN AS S_DEVICE23_YN,BB.S_DEVICE08_CD AS S_DEVICE24_CD,BB.S_DEVICE08_YN AS S_DEVICE24_YN,BB.S_DEVICE09_CD AS S_DEVICE25_CD,BB.S_DEVICE09_YN AS S_DEVICE25_YN,BB.S_DEVICE10_CD AS S_DEVICE26_CD,BB.S_DEVICE10_YN AS S_DEVICE26_YN,
            BB.S_DEVICE11_CD AS S_DEVICE27_CD,BB.S_DEVICE11_YN AS S_DEVICE27_YN,BB.S_DEVICE12_CD AS S_DEVICE28_CD,BB.S_DEVICE12_YN AS S_DEVICE28_YN,BB.S_DEVICE13_CD AS S_DEVICE29_CD,BB.S_DEVICE13_YN AS S_DEVICE29_YN,BB.S_DEVICE14_CD AS S_DEVICE30_CD,BB.S_DEVICE14_YN AS S_DEVICE30_YN,BB.S_DEVICE15_CD AS S_DEVICE31_CD,BB.S_DEVICE15_YN AS S_DEVICE31_YN,BB.S_DEVICE16_CD AS S_DEVICE32_CD,BB.S_DEVICE16_YN AS S_DEVICE32_YN
        FROM
        (SELECT
            CONCAT(td.S_DEVICE_ID,'02')  as GW_ID,DATE_FORMAT(SYSDATE(), '%Y%m%d%H%i00') as DATE,td.S_SITE_ID,right(td.S_SITE_ID,3) as S_PREVENT_CD,
            CASE WHEN left(tss.S_DEVICE01_CD, 2) = '차압' THEN 'D0' ELSE 'D0' END as S_DEVICE01_CD,tss.S_DEVICE01_YN,
            CASE WHEN left(tss.S_DEVICE02_CD, 2) = '차압' THEN 'D0' ELSE 'D0' END as S_DEVICE02_CD,tss.S_DEVICE02_YN,
            CASE WHEN left(tss.S_DEVICE03_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE03_CD,tss.S_DEVICE03_YN,
            CASE WHEN left(tss.S_DEVICE04_CD, 2) = 'PH' THEN 'H0' ELSE 'H0' END as S_DEVICE04_CD,tss.S_DEVICE04_YN,
            CASE WHEN left(tss.S_DEVICE05_CD, 2) = 'PH' THEN 'H0' ELSE 'H0' END as S_DEVICE05_CD,tss.S_DEVICE05_YN,
            CASE WHEN left(tss.S_DEVICE06_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE06_CD,tss.S_DEVICE06_YN,
            CASE WHEN left(tss.S_DEVICE07_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE07_CD,tss.S_DEVICE07_YN,
            CASE WHEN left(tss.S_DEVICE08_CD, 2) = '방지' THEN 'A0' ELSE 'A0' END as S_DEVICE08_CD,tss.S_DEVICE08_YN,
            CASE WHEN left(tss.S_DEVICE09_CD, 2) = '방지' THEN 'A0' ELSE 'A0' END as S_DEVICE09_CD,tss.S_DEVICE09_YN,
            CASE WHEN left(tss.S_DEVICE10_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE10_CD,tss.S_DEVICE10_YN,
            CASE WHEN left(tss.S_DEVICE11_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE11_CD,tss.S_DEVICE11_YN,
            CASE WHEN left(tss.S_DEVICE12_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE12_CD,tss.S_DEVICE12_YN,
            CASE WHEN left(tss.S_DEVICE13_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE13_CD,tss.S_DEVICE13_YN,
            CASE WHEN left(tss.S_DEVICE14_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE14_CD,tss.S_DEVICE14_YN,
            CASE WHEN left(tss.S_DEVICE15_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE15_CD,tss.S_DEVICE15_YN,
            CASE WHEN left(tss.S_DEVICE16_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE16_CD,tss.S_DEVICE16_YN
        FROM sensor.T_DEVICE td, sensor.T_SENSE_SET1 tss 
        WHERE tss.id_ad_num='1') AA,
        (SELECT
            CONCAT(td.S_DEVICE_ID,'02')  as GW_ID,DATE_FORMAT(SYSDATE(), '%Y%m%d%H%i00') as DATE,td.S_SITE_ID,right(td.S_SITE_ID,3) as S_PREVENT_CD,
            CASE WHEN left(tss.S_DEVICE01_CD, 2) = '차압' THEN 'D0' ELSE 'D0' END as S_DEVICE01_CD,tss.S_DEVICE01_YN,
            CASE WHEN left(tss.S_DEVICE02_CD, 2) = '차압' THEN 'D0' ELSE 'D0' END as S_DEVICE02_CD,tss.S_DEVICE02_YN,
            CASE WHEN left(tss.S_DEVICE03_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE03_CD,tss.S_DEVICE03_YN,
            CASE WHEN left(tss.S_DEVICE04_CD, 2) = 'PH' THEN 'H0' ELSE 'H0' END as S_DEVICE04_CD,tss.S_DEVICE04_YN,
            CASE WHEN left(tss.S_DEVICE05_CD, 2) = 'PH' THEN 'H0' ELSE 'H0' END as S_DEVICE05_CD,tss.S_DEVICE05_YN,
            CASE WHEN left(tss.S_DEVICE06_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE06_CD,tss.S_DEVICE06_YN,
            CASE WHEN left(tss.S_DEVICE07_CD, 2) = '온도' THEN 'T0' ELSE 'T0' END as S_DEVICE07_CD,tss.S_DEVICE07_YN,
            CASE WHEN left(tss.S_DEVICE08_CD, 2) = '방지' THEN 'A0' ELSE 'A0' END as S_DEVICE08_CD,tss.S_DEVICE08_YN,
            CASE WHEN left(tss.S_DEVICE09_CD, 2) = '방지' THEN 'A0' ELSE 'A0' END as S_DEVICE09_CD,tss.S_DEVICE09_YN,
            CASE WHEN left(tss.S_DEVICE10_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE10_CD,tss.S_DEVICE10_YN,
            CASE WHEN left(tss.S_DEVICE11_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE11_CD,tss.S_DEVICE11_YN,
            CASE WHEN left(tss.S_DEVICE12_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE12_CD,tss.S_DEVICE12_YN,
            CASE WHEN left(tss.S_DEVICE13_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE13_CD,tss.S_DEVICE13_YN,
            CASE WHEN left(tss.S_DEVICE14_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE14_CD,tss.S_DEVICE14_YN,
            CASE WHEN left(tss.S_DEVICE15_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE15_CD,tss.S_DEVICE15_YN,
            CASE WHEN left(tss.S_DEVICE16_CD, 2) = '배출' THEN 'A1' ELSE 'A1' END as S_DEVICE16_CD,tss.S_DEVICE16_YN
        FROM sensor.T_DEVICE td, sensor.T_SENSE_SET1 tss 
        WHERE tss.id_ad_num='2')BB;
        '''

        db_datas = db_session.execute(sql)
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
            
            message.extend(data.GW_ID.encode("ASCII")) #게이트 ID
            message.extend(':'.encode("ASCII"))

            message.extend(data.S_SITE_ID.encode("ASCII"))	#사업장
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_PREVENT_CD.encode("ASCII"))	#굴뚝번호
            message.extend(':'.encode("ASCII"))
            message.extend(data.DATE.encode("ASCII"))	#시간
            message.extend(':'.encode("ASCII"))
            
            message.extend(data.S_DEVICE01_CD.encode("ASCII"))	#4~20mA
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE01_YN.encode("ASCII"))	#사용여부
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE02_CD.encode("ASCII"))	#4~20mA
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE02_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE03_CD.encode("ASCII"))	#4~20mA
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE03_YN.encode("ASCII"))	#사용여부
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE04_CD.encode("ASCII"))	#4~20mA
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE04_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE05_CD.encode("ASCII"))	#4~20mA
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE05_YN.encode("ASCII"))	#사용여부
            message.extend(':'.encode("ASCII"))
            
            message.extend(data.S_DEVICE06_CD.encode("ASCII"))	#pt100
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE06_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE07_CD.encode("ASCII"))	#pt100
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE07_YN.encode("ASCII"))	#사용여부
            message.extend(':'.encode("ASCII"))
            
            message.extend(data.S_DEVICE08_CD.encode("ASCII"))	#전류1
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE08_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE09_CD.encode("ASCII"))	#전류2
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE09_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE10_CD.encode("ASCII"))	#전류3
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE10_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE11_CD.encode("ASCII"))	#전류4
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE11_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE12_CD.encode("ASCII"))	#전류5
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE12_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE13_CD.encode("ASCII"))	#전류6
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE13_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE14_CD.encode("ASCII"))	#전류7
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE14_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE15_CD.encode("ASCII"))	#전류8
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE15_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE16_CD.encode("ASCII"))	#전류9
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE16_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            
            #message.extend(data.S_DEVICE17_CD.encode("ASCII"))	#4~20mA
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE17_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE18_CD.encode("ASCII"))	#4~20mA
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE18_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE19_CD.encode("ASCII"))	#4~20mA
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE19_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE20_CD.encode("ASCII"))	#4~20mA
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE20_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE21_CD.encode("ASCII"))	#4~20mA
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE21_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE22_CD.encode("ASCII"))	#pt100
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE22_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE23_CD.encode("ASCII"))	#pt100
            #message.extend(':'.encode("ASCII"))
            #message.extend(data.S_DEVICE23_YN.encode("ASCII"))	#사용여부    
            #message.extend(':'.encode("ASCII"))
            
            message.extend(data.S_DEVICE24_CD.encode("ASCII"))	#전류1
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE24_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE25_CD.encode("ASCII"))	#전류2
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE25_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE26_CD.encode("ASCII"))	#전류3
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE26_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE27_CD.encode("ASCII"))	#전류4
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE27_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE28_CD.encode("ASCII"))	#전류5
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE28_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE29_CD.encode("ASCII"))	#전류6
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE29_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE30_CD.encode("ASCII"))	#전류7
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE30_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            
            message.extend(data.S_DEVICE24_CD.encode("ASCII"))	#전류8
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE24_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE25_CD.encode("ASCII"))	#전류9
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE25_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE26_CD.encode("ASCII"))	#전류10
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE26_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE27_CD.encode("ASCII"))	#전류11
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE27_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE28_CD.encode("ASCII"))	#전류12
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE28_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE29_CD.encode("ASCII"))	#전류13
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE29_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE30_CD.encode("ASCII"))	#전류14
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE30_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE31_CD.encode("ASCII"))	#전류15
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE31_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            message.extend(data.S_DEVICE32_CD.encode("ASCII"))	#전류16
            message.extend(','.encode("ASCII"))
            message.extend(data.S_DEVICE32_YN.encode("ASCII"))	#사용여부    
            message.extend(':'.encode("ASCII"))
            

            message.extend('Tpm2+NPl/SYPq84leQ3MwVcSLl435284R+E6vZlYFDE=<EOF>'.encode("ASCII"))	#etx
            #message.extend('\x03'.encode("ASCII"))	#etx


            print(message)
            

            # 메시지를 전송합니다.
            print("메시지 전송")
            
            client_socket.send(message)
            
        # 메시지를 수신합니다.
        db_datas = client_socket.recv(1024)
        print('Received', repr(db_datas.decode()))

            
        break
            

                
        
	

	#

# 소켓을 닫습니다.
client_socket.close()


