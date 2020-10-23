import sys
from pymsgbox import alert, confirm
from threading import Thread
from .usb_detector import USBHotplugDetector
from PyQt5 import QtCore, QtGui, QtWidgets


usb_detector = USBHotplugDetector()


class HeimdallMainWindow(object):
    def __init__(self):
        self.is_started = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(989, 671)

        small_font = QtGui.QFont()
        small_font.setPointSize(12)

        large_font = QtGui.QFont()
        large_font.setPointSize(14)

        self.threadpool = QtCore.QThreadPool()
        
        sys.stdout = WritingStream(outputted_text=self.normal_write_text)

        MainWindow.setStyleSheet("background-color: rgba(255, 255, 255, 253)")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        
        icon = QtGui.QIcon()
        
        MainWindow.setProperty("icon", icon)
 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.main_grid = QtWidgets.QGridLayout()
        self.main_grid.setHorizontalSpacing(40)
        self.main_grid.setVerticalSpacing(20)
        self.main_grid.setObjectName("main_grid")
        self.label = QtWidgets.QLabel(self.centralwidget)
 
        self.label.setFont(large_font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        self.main_grid.addWidget(self.label, 3, 0, 1, 1)
 
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_grid.addItem(spacer_item, 0, 3, 1, 1)
        spacer_item_one = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.main_grid.addItem(spacer_item_one, 2, 1, 1, 1)
        spacer_item_two = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.main_grid.addItem(spacer_item_two, 0, 0, 1, 1)
        
        self.start_evaluator_btn = QtWidgets.QPushButton(self.centralwidget)
 
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.start_evaluator_btn.sizePolicy().hasHeightForWidth())
 
        self.start_evaluator_btn.setSizePolicy(size_policy)
        self.start_evaluator_btn.setMinimumSize(QtCore.QSize(200, 50))
 
        font = QtGui.QFont()
        font.setPointSize(14)
 
        self.start_evaluator_btn.setFont(large_font)
        self.start_evaluator_btn.setStyleSheet("background: white;\n"
            "color: black;\n"
            ""
            )
        
        self.start_evaluator_btn.setObjectName("start_evaluator_btn")
        self.main_grid.addWidget(self.start_evaluator_btn, 0, 1, 1, 1)
        self.stop_evaluator_btn = QtWidgets.QPushButton(self.centralwidget)
        
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.stop_evaluator_btn.sizePolicy().hasHeightForWidth())
        
        self.stop_evaluator_btn.setSizePolicy(size_policy)
        self.stop_evaluator_btn.setMinimumSize(QtCore.QSize(200, 50))
        
        self.stop_evaluator_btn.setFont(large_font)
        self.stop_evaluator_btn.setStyleSheet("background: white;\n"
            "color: black;"
            )
        
        self.stop_evaluator_btn.setObjectName("stop_evaluator_btn")
        self.main_grid.addWidget(self.stop_evaluator_btn, 0, 2, 1, 1)
        self.logs_text_box = QtWidgets.QTextEdit(self.centralwidget)

       
        self.logs_text_box.setFont(small_font)
        self.logs_text_box.setStyleSheet("background: white;\n" 
        "color: black;"
        )

        self.logs_text_box.setReadOnly(True)
        self.logs_text_box.setAcceptRichText(False)
        self.logs_text_box.setObjectName("logs_text_box")
        self.logs_text_box.moveCursor(QtGui.QTextCursor.End)
        self.main_grid.addWidget(self.logs_text_box, 4, 0, 1, 4)
       
        self.gridLayout.addLayout(self.main_grid, 1, 0, 1, 1)
        spacer_item_three = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacer_item_three, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
       
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "USB Threat Evaluator"))
        
        self.label.setText(_translate("MainWindow", "Logs:"))
        self.start_evaluator_btn.setText(_translate("MainWindow", "Start Evaluator"))
        self.stop_evaluator_btn.setText(_translate("MainWindow", "Stop Evaluator"))

        self.start_evaluator_btn.clicked.connect(self.__start_evaluator)
        self.stop_evaluator_btn.clicked.connect(self.__stop_evaluator)

    def normal_write_text(self, text):
        cursor = self.logs_text_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logs_text_box.setTextCursor(cursor)
        self.logs_text_box.ensureCursorVisible()
    
    def __start_evaluator(self):
        if self.is_started:
            print('>>> Evaluator has already been started.')
        else:
            worker = GuiThreadWorker()
            self.threadpool.start(worker)
            self.is_started = True
            self.start_evaluator_btn.setEnabled(False)
            self.stop_evaluator_btn.setEnabled(True)

    def __stop_evaluator(self):
        usb_detector.stop()
        self.start_evaluator_btn.setEnabled(True)
        self.stop_evaluator_btn.setEnabled(False)


class WritingStream(QtCore.QObject):
    outputted_text = QtCore.pyqtSignal(str)

    def write(self, text):
        self.outputted_text.emit(str(text))

class GuiThreadWorker(QtCore.QRunnable):
    @QtCore.pyqtSlot()
    def run(self):
        usb_detector.start()

def show_gui(fullscreen=True):
    app = QtWidgets.QApplication(sys.argv)
    heimdall_app = QtWidgets.QMainWindow()

    ui = HeimdallMainWindow()
    ui.setupUi(heimdall_app)

    if fullscreen:
        heimdall_app.showFullScreen()
    else:
        heimdall_app.show()

    sys.exit(app.exec_())

def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)

def show_confirm_box(box_title, box_content, displayed_buttons = ['Yes', 'No']):
    result = confirm(text=box_content, title=box_title, buttons=displayed_buttons)
    
    if result == 'OK':
        return True
    else:
        return False
        