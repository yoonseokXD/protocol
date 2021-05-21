import sys, threading, os, datetime, time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime
from mylogger import logger
from setting_ip import SettingIPUI
from monitoring import MonitoringUI
#from detail_ui import DetailUI
from connection_status import ConnectionStatusUI
from gl_protocol import asyncio_client
from setting_password import SettingPasswordUI
from setting_device_sensor import SettingDeviceSensorUI
from config import Config as Config
from db.database import Database
from db.models import TDEVICE, TCODE

DEL_SEQ_TIME = time.strftime("%H")


#서버시간 동기화
def TimeSyncThread() :
    timer = threading.Timer(3600, TimeSyncThread)
    os.system("python3 tcp_socket_client_sync.py")
    os.system("python3 data_delete_day.py")
    print("동기화 및 삭제 완료")
    timer.setDaemon(True)
    timer.start()
    if DEL_SEQ_TIME == "00" :
        DataDeleteThread()
    
# 오래된 데이터 삭제
def DataDeleteThread() :
        os.system("python3 data_delete_month.py")
        print("장기보관 데이터 삭제")
    
def async_run() :
	asyncio_client.run_client()


form_class = uic.loadUiType("./ui/2_main.ui")[0]



UI_MOVE = {"HOME":0, "MONITORING":1, "STATUS":2, "SETTING":3}

class MainWindow(QMainWindow, form_class):
    style_button_active = 'QPushButton:hover:!pressed{\nbackground-color:rgb(2, 43, 90);\nborder:0px;\n}\nQPushButton{\nborder:2px solid rgb(19, 51, 76);\nbackground-color:rgb(38, 32, 135);\ncolor:white;\nborder-radius: 5px;\npadding:3 3 3 3;\nfont-size:18px;\n}'
    style_button_deactive = 'QPushButton:hover:!pressed{\nbackground-color:rgb(2, 43, 90);\nborder:0px;\n}\nQPushButton{\nborder:2px solid rgb(19, 51, 76);\nbackground-color:rgb(2,16,36);\ncolor:white;\nborder-radius: 5px;\npadding:3 3 3 3;\nfont-size:18px;\n}'
    config = None

    monitoring_ui = None
    status_ui = None
    setting_password_ui = None
    ip_ui = None
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config = Config()

        self.db_session = Database.getSession()
        self.device_info = self.db_session.query(TDEVICE).limit(1)[0]
        logger.info("device info (DB) : {}".format(self.device_info.__dict__))

        ##timer 시작
        self.timerStart()

        ##button event 등록
        #head 이벤트
        self.label_home.clicked.connect(self.homeClicked)
        self.label_home_title.clicked.connect(self.homeClicked)
        self.button_monitor.clicked.connect(self.monitorClicked)
        self.button_monitor.mousePressEvent = self.monitorClicked
        #self.button_status.clicked.connect(self.statusClicked)
        #self.button_status.mousePressEvent = self.statusClicked
        self.button_setting.clicked.connect(self.settingClicked)
        self.button_setting.mousePressEvent = (self.settingClicked)
        self.button_settingip.mousePressEvent = (self.ipClicked)
        #main 이벤트
        self.label_monitoring.clicked.connect(self.monitorClicked)
        self.label_setting.clicked.connect(self.settingClicked)
        #self.label_status.clicked.connect(self.statusClicked)

        self.label_home_title.setText(self.device_info.S_SITE_NM)
        self.allButtonDeactive()

        #초기 시작 시 모니니터링 화면으로 이동
        self.monitorClicked(None)

    #홈화면 버튼 클릭
    def homeClicked(self):
       logger.info("homeClicked")
       self.allButtonDeactive()
       self.main_stackedWidget.setCurrentIndex(0)
       self.label_home.setFocus()

    #모니터링 화면 버튼 클릭
    def monitorClicked(self, event=None):
        logger.info("monitorClicked")

        if(self.monitoring_ui != None):
            self.monitoring_ui.deleteLater()
            self.monitoring_ui.destroy()

        self.monitoring_ui = MonitoringUI(self)
        self.main_stackedWidget.addWidget(self.monitoring_ui)
        self.main_stackedWidget.setCurrentWidget(self.monitoring_ui)

        self.allButtonDeactive()
        self.button_monitor.setStyleSheet(self.style_button_active)
        self.button_monitor.setFocus()

    # 통신상태 버튼 클릭
    def statusClicked(self, event=None):
        logger.info("statusClicked")

        if (self.status_ui != None):
            logger.info("delete status ")
            self.status_ui.setParent(None)
            self.status_ui.deleteLater()
            self.status_ui.destroy()

        self.status_ui = ConnectionStatusUI(self)
        self.main_stackedWidget.addWidget(self.status_ui)
        self.main_stackedWidget.setCurrentWidget(self.status_ui)

        self.allButtonDeactive()
        self.button_status.setStyleSheet(self.style_button_active)
        self.button_status.setFocus()
    #ip설정버튼 클릭
    def ipClicked(self, event=None):
        logger.info("eipClicked")
        if(self.ip_ui != None):
            self.ip_ui.deleteLater()
            self.ip_ui.destroy()

        self.ip_ui = SettingIPUI(self)
        self.main_stackedWidget.addWidget(self.ip_ui)
        self.main_stackedWidget.setCurrentWidget(self.ip_ui)

        self.allButtonDeactive()
        self.button_settingip.setStyleSheet(self.style_button_active)
        self.button_settingip.setFocus()
        
    #설정 버튼 클릭
    def settingClicked(self,event=None):
        logger.info("settingClicked")

        if (self.setting_password_ui != None):
            self.setting_password_ui.deleteLater()
            self.setting_password_ui.destroy()

        self.setting_password_ui = SettingPasswordUI(self)
        self.main_stackedWidget.addWidget(self.setting_password_ui)
        self.main_stackedWidget.setCurrentWidget(self.setting_password_ui)

        self.allButtonDeactive()
        self.button_setting.setStyleSheet(self.style_button_active)
        self.button_setting.setFocus()




    def allButtonDeactive(self):
        self.button_setting.setStyleSheet(self.style_button_deactive)
        #self.button_status.setStyleSheet(self.style_button_deactive) 
        self.button_monitor.setStyleSheet(self.style_button_deactive)





    # 상단 시간 변경
    def updateTime(self):
        self.labelTime.setText(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

    def timerStart(self):
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000) # update every second


if __name__ == "__main__":
    TimeSyncThread()
    os.system("python3 gl_protocol.py")
    app = QApplication(sys.argv)
    app.setFont(QFont("NanumGothic"))
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use



    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()







