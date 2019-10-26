from usb_detector import USBHotplugDetector
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HeimdallApp(object):
    def setupUi(self, HeimdallApp):
        HeimdallApp.setObjectName("HeimdallApp")
        HeimdallApp.resize(851, 595)

        usb_detector = USBHotplugDetector()

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

        self.start_evaluator_btn.clicked.connect(usb_detector.start())
        self.stop_evaluator_btn.clicked.connect(usb_detector.stop())

    def retranslateUi(self, HeimdallApp):
        _translate = QtCore.QCoreApplication.translate
        HeimdallApp.setWindowTitle(_translate("HeimdallApp", "Heimdall"))
        self.start_evaluator_btn.setText(_translate("HeimdallApp", "Start Evaluator"))
        self.stop_evaluator_btn.setText(_translate("HeimdallApp", "Stop Evaluator"))
        self.logs_label.setText(_translate("HeimdallApp", "Logs:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HeimdallApp = QtWidgets.QMainWindow()
    ui = Ui_HeimdallApp()
    ui.setupUi(HeimdallApp)
    HeimdallApp.show()
    sys.exit(app.exec_())

