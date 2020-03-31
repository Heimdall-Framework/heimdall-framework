import sys
from pymsgbox import alert
from threading import Thread
from usb_detector import USBHotplugDetector
from PyQt5 import QtCore, QtGui, QtWidgets


usb_detector = USBHotplugDetector()
#evaluator_thread = Thread(target=usb_detector.start)

class Ui_HeimdallApp(object):
    def setupUi(self, HeimdallApp):
        self.threadpool = QtCore.QThreadPool()

        HeimdallApp.setObjectName("HeimdallApp")
        HeimdallApp.resize(851, 595)
        
        sys.stdout = WritingStream(outputed_text=self.normal_write_text)
        
        self.centralwidget = QtWidgets.QWidget(HeimdallApp)
        self.centralwidget.setObjectName("centralwidget")

        self.start_evaluator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_evaluator_btn.setGeometry(QtCore.QRect(340, 80, 161, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.start_evaluator_btn.setFont(font)
        self.start_evaluator_btn.setObjectName("start_evaluator_btn")

        self.stop_evaluator_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_evaluator_btn.setGeometry(QtCore.QRect(340, 140, 161, 37))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stop_evaluator_btn.setFont(font)
        self.stop_evaluator_btn.setObjectName("stop_evaluator_btn")

        self.logs_text_box = QtWidgets.QTextEdit(self.centralwidget)
        self.logs_text_box.setGeometry(QtCore.QRect(10, 270, 831, 311))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.logs_text_box.setFont(font)
        self.logs_text_box.setObjectName("logs_text_box")

        self.logs_label = QtWidgets.QLabel(self.centralwidget)
        self.logs_label.setGeometry(QtCore.QRect(20, 240, 64, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.logs_label.setFont(font)
        self.logs_label.setObjectName("logs_label")
        
        HeimdallApp.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(HeimdallApp)
        self.statusbar.setObjectName("statusbar")
        
        HeimdallApp.setStatusBar(self.statusbar)

        self.retranslateUi(HeimdallApp)
        QtCore.QMetaObject.connectSlotsByName(HeimdallApp)

    def retranslateUi(self, HeimdallApp):
        _translate = QtCore.QCoreApplication.translate
        HeimdallApp.setWindowTitle(_translate("HeimdallApp", "Heimdall"))
        self.start_evaluator_btn.setText(_translate("HeimdallApp", "Start Evaluator"))
        self.stop_evaluator_btn.setText(_translate("HeimdallApp", "Stop Evaluator"))
        self.logs_label.setText(_translate("HeimdallApp", "Logs:"))

        self.start_evaluator_btn.clicked.connect(self.__start_evaluator)
        self.stop_evaluator_btn.clicked.connect(self.__stop_evaluator)
    
    def normal_write_text(self, text):
        cursor = self.logs_text_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logs_text_box.setTextCursor(cursor)
        self.logs_text_box.ensureCursorVisible()
    
    def __start_evaluator(self):
        worker = GuiThreadWorker()
        self.threadpool.start(worker) 

    def __stop_evaluator(self):
        usb_detector.stop()
        
    

class WritingStream(QtCore.QObject):
    outputed_text = QtCore.pyqtSignal(str)

    def write(self, text):
        self.outputed_text.emit(str(text))

class GuiThreadWorker(QtCore.QRunnable):
    @QtCore.pyqtSlot()
    def run(self):
        usb_detector.start()

def show_gui():
    app = QtWidgets.QApplication(sys.argv)
    HeimdallApp = QtWidgets.QMainWindow()

    ui = Ui_HeimdallApp()
    ui.setupUi(HeimdallApp)

    HeimdallApp.show()
    sys.exit(app.exec_())


def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)