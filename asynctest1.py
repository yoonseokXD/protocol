import hashlib, os, socket, threading, time, datetime, binascii, asyncio, sys, threading
from multiprocessing import Queue
from crccheck.crc import Crc, Crc16Ccitt
from dateutil.parser import parse
import ctypes, paramiko
from array import *
import sqlalchemy
from db.database import Database



kisa_seed_cbc = ctypes.cdll.LoadLibrary("./kisa_seed_cbc.so")
clib_sha = ctypes.cdll.LoadLibrary("./kisa_sha256.so")
clib_crc = ctypes.cdll.LoadLibrary("./crc16ccitt.so")
gb_sql = '''
SELECT left(S_SITE_ID,7) S_SITE_ID /*사업장id */
,right(S_SITE_ID,3) as S_PREVENT_CD /*굴뚝번호 */ from T_DEVICE
'''
db_session = Database.getSession()
gb_session = Database.getSession()
rs = list(gb_session.execute(gb_sql))
print(rs)
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

db_id = rs[0]  # sql alchemy 통해서 사업장 id, 굴뚝번호 가져와야함.
cmcode = rs[1]
JEJO_CODE = 'WB'
        

### Query List ####################################################
TCNG_count = '''
select A.cnt + B.cnt + C.cnt + D.cnt + E.cnt + F.cnt + G.cnt + H.cnt + I.cnt + J.cnt + K.cnt + L.cnt + M.cnt + N.cnt + O.cnt + P.cnt as tot_cnt FROM /*항목수 */
(select count(S_DEVICE01_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE01_YN = 'Y') A,
(select count(S_DEVICE02_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE02_YN = 'Y') B,
(select count(S_DEVICE03_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE03_YN = 'Y') C,
(select count(S_DEVICE04_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE04_YN = 'Y') D,
(select count(S_DEVICE05_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE05_YN = 'Y') E,
(select count(S_DEVICE06_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE06_YN = 'Y') F,
(select count(S_DEVICE07_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE07_YN = 'Y') G,
(select count(S_DEVICE08_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE08_YN = 'Y') H,
(select count(S_DEVICE09_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE09_YN = 'Y') I,
(select count(S_DEVICE10_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE10_YN = 'Y') J,
(select count(S_DEVICE11_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE11_YN = 'Y') K,
(select count(S_DEVICE12_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE12_YN = 'Y') L,
(select count(S_DEVICE13_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE13_YN = 'Y') M,
(select count(S_DEVICE14_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE14_YN = 'Y') N,
(select count(S_DEVICE15_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE15_YN = 'Y') O,
(select count(S_DEVICE16_YN) cnt from sensor.T_SENSE_SET1 tss 
where S_DEVICE16_YN = 'Y') P
'''

###################################################################
async def run_server():
    server = await asyncio.start_server(handler, host='44.158.7.162', port='9090')
    if server is not None:
        print('server start')
        await server.wait_closed()
        print('server closed')

async def handler(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    #schedule.every().day.at("00:01").do(msg_handler.TVER())
    while 1 :
        #schedule.run_pending()
        data = await reader.read(1024)
        peername = writer.get_extra_info('peername')
        try:
            dcd_data = data[:-2].decode()
        except :
            dcd_data = data[:4].decode()
        if dcd_data[0:4] == 'PVER' :
            writer.write(msg_handler.DVER())
            await writer.drain()     
            
            acknak = await reader.read(1024)
            
            print('acknak:', acknak)
            if acknak == b'\x06' :
                writer.write(msg_handler.EOT())
                await writer.drain()
            elif acknak == b'\x15' :
                writer.write(msg_handler.DVER())
                await writer.drain()
            break
        elif dcd_data[0:4] == 'PDUM' :
            start_day = dcd_data[18:28]
            end_day = dcd_data[28:]
            sql = '''
            SELECT left(TD.S_SITE_ID,7) S_SITE_ID, right(TD.S_SITE_ID,3) as S_PREVENT_CD 
,CONCAT(substring(DATE_FORMAT(asd.value_date , '%y%m%d%H%i'),1,9) , case when substring(DATE_FORMAT(asd.value_date , '%i'),2) between '0' and '4' then '0' else '5' end) AS S_MEASURE_DATE 
,tss.S_DEVICE01_YN,tss.S_DEVICE01_NUMBER ,'D' as S_DEVICE01_CODE  ,CASE WHEN asd.ch1_4_20ma = '0' THEN '0' ELSE CONCAT(ROUND(AVG(31.25*(asd.ch1_4_20ma)-125),2)) END as S_DEVICE1_VALUE ,'0' as S_DEVICE1_STATE
,tss.S_DEVICE02_YN,tss.S_DEVICE02_NUMBER ,'D' as S_DEVICE02_CODE  ,CASE WHEN asd.ch2_4_20ma = '0.00' THEN '0' ELSE CONCAT(ROUND(AVG(31.25*(asd.ch2_4_20ma)-125),2)) END as S_DEVICE2_VALUE ,'0' as S_DEVICE2_STATE
,tss.S_DEVICE03_YN,tss.S_DEVICE03_NUMBER ,'T' as S_DEVICE03_CODE  ,CASE WHEN asd.ch3_4_20ma = '0.00' THEN '0' ELSE CONCAT(ROUND(AVG(550*((asd.ch3_4_20ma)-4)/16+(-50)),2)) END as S_DEVICE3_VALUE ,'0' as S_DEVICE3_STATE
,tss.S_DEVICE04_YN,tss.S_DEVICE04_NUMBER ,'H' as S_DEVICE04_CODE  ,CASE WHEN asd.ch4_4_20ma = '0.00' THEN '0' ELSE CONCAT(ROUND(AVG(0.875*(asd.ch4_4_20ma)-3.5),2)) END as S_DEVICE4_VALUE ,'0' as S_DEVICE4_STATE
,tss.S_DEVICE05_YN,tss.S_DEVICE05_NUMBER ,'H' as S_DEVICE05_CODE  ,CASE WHEN asd.ch5_4_20ma = '0.00' THEN '0' ELSE CONCAT(ROUND(AVG(0.875*(asd.ch5_4_20ma)-3.5),2)) END as S_DEVICE5_VALUE ,'0' as S_DEVICE5_STATE
,tss.S_DEVICE06_YN,tss.S_DEVICE06_NUMBER ,'T' as S_DEVICE06_CODE  ,case when left(asd.ch1_pt100,3) = '882' then '0' when left(asd.ch1_pt100,4) = '-242' then '0' ELSE asd.ch1_pt100 END S_DEVICE6_VALUE ,'0' as S_DEVICE6_STATE
,tss.S_DEVICE07_YN,tss.S_DEVICE07_NUMBER ,'T' as S_DEVICE07_CODE  ,case when left(asd.ch2_pt100,3) = '882' then '0' when left(asd.ch2_pt100,4) = '-242' then '0' ELSE asd.ch2_pt100 END S_DEVICE7_VALUE ,'0' as S_DEVICE7_STATE
,tss.S_DEVICE08_YN,tss.S_DEVICE08_NUMBER ,'A' as S_DEVICE08_CODE  ,CONCAT(AVG(csd.ch1_current)) as S_DEVICE8_VALUE  ,'0' as S_DEVICE8_STATE
,tss.S_DEVICE09_YN,tss.S_DEVICE09_NUMBER ,'A' as S_DEVICE09_CODE  ,CONCAT(AVG(csd.ch2_current)) as S_DEVICE9_VALUE  ,'0' as S_DEVICE9_STATE
,tss.S_DEVICE10_YN,tss.S_DEVICE10_NUMBER ,'A' as S_DEVICE10_CODE  ,CONCAT(AVG(csd.ch3_current)) as S_DEVICE10_VALUE  ,'0' as S_DEVICE10_STATE
,tss.S_DEVICE11_YN,tss.S_DEVICE11_NUMBER ,'A' as S_DEVICE11_CODE  ,CONCAT(AVG(csd.ch4_current)) as S_DEVICE11_VALUE  ,'0' as S_DEVICE11_STATE
,tss.S_DEVICE12_YN,tss.S_DEVICE12_NUMBER ,'A' as S_DEVICE12_CODE  ,CONCAT(AVG(csd.ch5_current)) as S_DEVICE12_VALUE  ,'0' as S_DEVICE12_STATE
,tss.S_DEVICE13_YN,tss.S_DEVICE13_NUMBER ,'A' as S_DEVICE13_CODE  ,CONCAT(AVG(csd.ch6_current)) as S_DEVICE13_VALUE  ,'0' as S_DEVICE13_STATE
,tss.S_DEVICE14_YN,tss.S_DEVICE14_NUMBER ,'A' as S_DEVICE14_CODE  ,CONCAT(AVG(csd.ch7_current)) as S_DEVICE14_VALUE  ,'0' as S_DEVICE14_STATE
,tss.S_DEVICE15_YN,tss.S_DEVICE15_NUMBER ,'A' as S_DEVICE15_CODE  ,CONCAT(AVG(csd.ch8_current)) as S_DEVICE15_VALUE  ,'0' as S_DEVICE15_STATE
,tss.S_DEVICE16_YN,tss.S_DEVICE16_NUMBER ,'A' as S_DEVICE16_CODE  ,CONCAT(AVG(csd.ch9_current)) as S_DEVICE16_VALUE  ,'0' as S_DEVICE16_STATE
FROM sensor.adc_sensor_data asd, sensor.ct_sensor_data csd, sensor.T_DEVICE TD , sensor.T_SENSE_SET1 tss 
where DATE_FORMAT(asd.value_date , '%y%m%d%H%i')  between '{}' and '{}' 
AND DATE_FORMAT(csd.value_date, '%y%m%d%H%i')  between '{}' and '{}' 
AND csd.group_id='1'
GROUP BY  TD.S_SITE_ID,  DATE_FORMAT(asd.value_date, '%Y-%m-%d %H:%i:00'),DATE_FORMAT(csd.value_date, '%Y-%m-%d %H:%i:00');
'''.format(start_day, end_day, start_day, end_day)
            dt = db_session.execute(sql)
            print(list(dt))
        elif dcd_data[0:4] == 'PTIM' :
            print(dcd_data)
            if dcd_data[16:18] == '32' :
                writer.write(msg_handler.ACK())
                await writer.drain()
                
                msg_handler.PSET(dcd_data[18:])
                ('time setting complete.')
            break
        elif dcd_data[0:4] == 'PUPG' :
            encrypted_data = CBC.decrypt(dcd_data[18:117])
            print('encrypted_data:', encrypted_data)
            break
        elif dcd_data[0:4] == 'PSET' :
            print(dcd_data)
            if dcd_data[16:18] == '32' :
                writer.write(msg_handler.ACK())
                await writer.drain()
                msg_handler.PSET(dcd_data[18:])
                ('time setting complete.')
            else :
                print(dcd_data, dcd_data[16:18], type(dcd_data[14:18]))
            break
        elif dcd_data[0:4] == 'PSEP' :
            if len(data) == 36 :
                writer.write(msg_handler.ACK())
                await writer.drain()
            else : 
                writer.write(msg_handler.NAK())
                await writer.drain()
            encrypted_string = data[18:-2]
            print(data[18:-2])
            password = CBC.PSEP_decrypt(encrypted_string)
            #password sql
            pw_sql = '''                                                        
            update sensor.T_DEVICE SET S_PASSWORD = '{}'
            where S_PASSWORD is not NULL ;
            commit;'''.format(password)
            db_session.execute(pw_sql)
            
            break
           
'''
async def handle_asyncclient(reader, writer):
    print('client :', writer.get_extra_info('peername'))
    while True:
        data = await reader.read(1024)
        print(data)
        dec_data = data[:-2].decode()
        print(data[:-2].decode())
        if dec_data[0:4] == 'PVER' :
            send = msg_handler.DVER()
            writer.write(send)
            await writer.drain()
        break
    writer.close()
    print('connection was closed')
    
async def server_asyncmain():
    server = await asyncio.start_server(handle_asyncclient,'44.158.7.162',9090)  
    if server is not None:
        print('server started')
        #
        await asyncio.sleep(60)
        server.close()
        await server.wait_closed()
        print('server was closed')


async def send_client(input_msg):
    try:
        reader, writer = await asyncio.open_connection(host='10.101.151.158',port=5010)
        print('connection')
        
        if input_msg[0:4] == "PVER" :
            send = msg_handler.DVER()
        writer.write(send)
        await writer.drain()
        print('send:', send)
        writer.close()
            
        
    except OSError:
        print('connection fail')
        return
'''
class msg_handler:
    def ACK():
        ACK = '\x06'.encode()
        msg = bytearray(ACK)
        return msg

    def NAK():
        NAK = '\x15'.encode()
        msg = bytearray(NAK)
        return msg

    def EOT():
        EOT = '\x04'.encode()
        msg = bytearray(EOT)
        return msg

    def version_info():
        pass

    def TDUM():
        msgName = order[2]
        siteCode = db_id
        preventCode = cmcode

    def TVER():
        msgName = order[5]
        siteCode = db_id
        preventCode = cmcode
        manufacCode = JEJO_CODE
        msgLength = 58
        verNumber = "1.01"

        headerMsg = "%4s%7s%3s%4d" %(msgName, siteCode, preventCode, msgLength)
        encodedString = headerMsg.encode()
        headerMsgArray = bytearray(encodedString)

        sha256InputData = (ctypes.c_ubyte * len(headerMsgArray))(*headerMsgArray)
        encResult = bytearray(32)
        encResult_c = (ctypes.c_ubyte * len(encResult))(*encResult)
        cfunc = ctypes.cdll.LoadLibrary("./kisa_sha256.so")
        cfunc.SHA256_Encrpyt(sha256InputData, len(headerMsg), encResult_c)
        
        encodedString = headerMsg.encode()
        sendMsg = bytearray(encodedString)
        encodedString = manufacCode.encode()
        sendMsg += bytearray(encodedString)
        sendMsg += encResult_c
        encodedString = verNumber.encode()
        sendMsg += bytearray(encodedString)

        crcInputData = (ctypes.c_ubyte * len(sendMsg))(*sendMsg)
        cfunc = ctypes.cdll.LoadLibrary("./crc16ccitt.so")
        crc16value = cfunc.crc16_ccitt(crcInputData, len(sendMsg))
        sendMsg += crc16value.to_bytes(2, byteorder="big")
        return sendMsg

    def SHA_256():
        with open('/root/sensor/main.py', 'rb') as crypt:
            s = crypt.read()
            sArray = bytearray(s)
            sha256InputData = (ctypes.c_ubyte * len(sArray))(*sArray)
            encResult = bytearray(32)
            encResult_c = (ctypes.c_ubyte * len(encResult))(*encResult)
            clib_sha.SHA256_Encrpyt(sha256InputData, len(s), encResult_c)
        return encResult_c
        
    def DVER(): #PVER 의 응답
        msgName = order[11]
        siteCode = db_id
        preventCode = cmcode
        manufacCode = JEJO_CODE
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
        return sendMsg

    def TCNG(): ###################
        msgName = order[9]
        siteCode = db_id
        preventCode = cmcode
        manufacCode = JEJO_CODE
        msgLength = 58
        verNumber = "1.01"
        encrypted_pw = CBC.PSEP_decrypt()
        headerMsg = "%4s%7s%3s%4d" %(msgName, siteCode, preventCode, msgLength)
        item_cnt_sql = ''' '''

    def TUPG(): #TUPG
        msgName = order[8]
        siteCode = db_id
        preventCode = cmcode
        msgLength = 56
        verNum = '1.01'

        headerMsg = "%4s%7s%3s%4d" %(msgName, siteCode, preventCode, msgLength)
        headerEncode = headerMsg.encode()
        
        msg = bytearray()      
        msg_type = order[8].encode('ascii') #전역변수 order 참조
        id_code = db_id
        client_version = ('2.03').encode('ascii') #메인 실행 프로그램으로부터 버전정보를 받아와야함.
        hash_code = bytes(msg_handler.SHA_256()) #메인 실행 프로그램을 해쉬화 해야함.
        CRC_len = 2
        msg_len = (('{}').format(len(msg_type)+len(id_code)+len(client_version)+len(hash_code)+CRC_len)).encode('ascii') #전체메세지길이
        
        CRC_code = hex(msg_handler.CRC16_CCITT(msg_type+id_code+msg_len, client_version+hash_code)).replace('0x','').upper() #오류검정코드
        print("msghandler :",CRC_code, type(CRC_code))
        msg.extend(msg_type)
        msg.extend(db_id)
        msg.extend(msg_len)
        msg.extend(client_version)
        msg.extend(hash_code)
        msg.extend(CRC_code.encode('ascii'))
        return msg

    def PSET(msg):
        time_string = msg
        ts = '20'+time_string
        z = str("'"+ts[0:4]+'-'+ts[4:6]+'-'+ts[6:8]+' '+ts[8:10]+':'+ts[10:12]+':'+ts[12:]+"'")
        os.system("date -s" + z)

class CBC(): 
  
    pbszUserKey = [0x0E9, 0x0F3, 0x094, 0x037, 0x00A, 0x0D4, 0x005, 0x089, 0x088, 0x0E3, 0x04F, 0x08F, 0x008, 0x017, 0x079, 0x0F1]
    pbszIV = [0x06F, 0x0BA, 0x0D9, 0x0FA, 0x036, 0x016, 0x025, 0x001, 0x026, 0x08D, 0x066, 0x0A7, 0x035, 0x0A8, 0x01A, 0x081]
    plainText = [0x00] * 231
    pbszCipherText = [0x00] * 210


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
    
        plainText = msg
        plainTextList = []
        for i in range(round((len(plainText))/2)) :
            plainTextList.append(int((plainText[2*i:2*i+2]),16))
        print("plainTextList:",plainTextList)
        plainText_array = (ctypes.c_ubyte * len(plainTextList))(*plainTextList)
        res_e = CBC.seed_cbc_encrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, plainText_array, len(CBC.PUPG_msg), CBC.pbszCipherText_array) # key, IV, 평문, 평문 길이, 암호문출력버퍼
        print("encrypt res :", res_e)
        encryptedTextArray = []
        encryptedHexArray = []
 
        range(0, res_e)
        for i in range(res_e):
            print(hex(int(CBC.pbszCipherText_array[i])), end=' ')
            encryptedTextArray.append(CBC.pbszCipherText_array[i])
        
        for i in range(len(encryptedTextArray)):
            encryptedHexArray.append((hex(encryptedTextArray[i])[2:]))
            if len(encryptedHexArray[i]) < 2 :
                encryptedHexArray[i] = '0'+encryptedHexArray[i]
        print("\r\n")
        print("encryptedTextArray:", encryptedTextArray)
        print("\r\n")
        
        print("encryptedHexArray:",encryptedHexArray)
        encryptedHexStr=''.join(encryptedHexArray)
        print("encryptedHexStr:", encryptedHexStr)
        return encryptedHexStr
        
    def encrypt_sample(msg) : # decrypt 함수의 암호문 길이를 리턴하기 위한 함수
        plainText = msg
        plainTextList = []
        for i in range(round((len(plainText))/2)) :
            plainTextList.append(int((plainText[2*i:2*i+2]),16))
        plainText_array = (ctypes.c_ubyte * len(plainTextList))(*plainTextList)
        res = CBC.seed_cbc_encrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, plainText_array, len(CBC.PUPG_msg), CBC.pbszCipherText_array) # key, IV, 평문, 평문 길이, 암호문출력버퍼
        print("encrypt res :", res)

        range(0, res)
        for i in range(res):
                print(hex(round(CBC.pbszCipherText_array[i])), end=' ')
        print(type(res))
        return res

    def decrypt(msg) :
        print("msg:", msg)
        inputEncryptedStr = msg
        print("inputEncryptedStr:", inputEncryptedStr)
        inputEncryptedStr_list = []
        print("inputEncryptedStr_list:", inputEncryptedStr_list)
        for i in range(round((len(inputEncryptedStr))/2)) :
            inputEncryptedStr_list.append((inputEncryptedStr[2*i:2*i+2]))
        print("inputEncryptedStr_list2:", inputEncryptedStr_list)
        intlist = []
        for i in range(len(inputEncryptedStr_list)):
            intlist.append(int(inputEncryptedStr_list[i],16))
        print("intlist:", intlist)
        input_array = (ctypes.c_ubyte * len(intlist))(*intlist)

        res_d = CBC.seed_cbc_decrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, input_array, CBC.encrypt_sample(inputEncryptedStr), CBC.plainText_array) # key, IV, 암호문, 암호문 길이, 평문출력버퍼

        decrypt_result = ''
        print("decrypt res :", res_d)
        
        for i in range(res_d):
                print(hex(CBC.plainText_array[i]), end=' ')
                decrypt_result+=chr(CBC.plainText_array[i])
                
        print("----\r\n")
        print("Dectypted Result:",decrypt_result)
        return decrypt_result

    def PSEP_decrypt(msg):
        PSEP_pw = '2323'
        PSEP_msg = "%10s"%(PSEP_pw)
        bPSEP_msg = bytes(PSEP_msg, 'utf-8')
        PSEP_array = (ctypes.c_ubyte * len(bPSEP_msg))(*bPSEP_msg)
        result = CBC.seed_cbc_decrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, msg, 16, PSEP_array)
        decrypted_pw = ''
        for ascode in PSEP_array :
        
            ch = chr(ascode)
            decrypted_pw+=ch
            decrypted_pw= decrypted_pw.lstrip()
        print(decrypted_pw)
        return decrypted_pw

    def PSEP_encrypt(): # db 의 암호를 SEED128-CBC방식으로 암호화 하여 리턴하는 함수.
        sql = ''' select S_PASSWORD from T_DEVICE '''
        db_data = db_session.execute(sql)
        db_pw = list(db_data)
        PSEP_pw = db_pw[0]
        print(PSEP_pw)
        PSEP_msg = "%10s"%(PSEP_pw)
        bPSEP_msg = bytes(PSEP_msg, 'utf-8')
        PSEP_array = (ctypes.c_ubyte * len(bPSEP_msg))(*bPSEP_msg)
        res = CBC.seed_cbc_encrypt(CBC.pbszUserKey_array, CBC.pbszIV_array, PSEP_msg, len(PSEP_msg), PSEP_array)# 평문, 평문 길이byte, 출력 버퍼 크기 byte
        H_PSEP_array = []
        for i in range(len(PSEP_array)):
            H_PSEP_array.append(hex(PSEP_array[i]))
        print(H_PSEP_array)
        H_PSEP_str = ''.join(H_PSEP_array)
        H_PSEP_str = H_PSEP_str.replace('0x','')
        print(H_PSEP_str)
        return H_PSEP_str


if __name__ == "__main__":
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        print('Async event loop already running')
        tsk = loop.create_task(run_server())
    else:
        print('Starting new event loop')
        loop.run_until_complete(run_server())   