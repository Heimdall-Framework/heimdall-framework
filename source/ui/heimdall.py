from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pymsgbox import alert, confirm
from threading import Thread
from .usb_detector import USBHotplugDetector
from PyQt5 import QtCore, QtGui, QtWidgets

usb_detector = USBHotplugDetector()

SMALL_FONT = 10
MEDIUM_FONT = 12
LARGE_FONT = 14

class HeimdallMainWindow(object):
    def __init__(self):
        self.is_started = False

    def setupUi(self, USBEvaluatorGui):
        USBEvaluatorGui.setObjectName("USBEvaluatorGui")
        USBEvaluatorGui.resize(800, 480)
        USBEvaluatorGui.setStyleSheet(
            "font: 12pt \"Nirmala UI\";\n"
            "color: white;\n"
            "background: #2c3e50;\n"
            "")

        self.threadpool = QtCore.QThreadPool()
        sys.stdout = WritingStream(outputted_text= self.normal_write_text)
            
        self.sidebar = QtWidgets.QWidget(USBEvaluatorGui)
        self.sidebar.setGeometry(QtCore.QRect(-6, 0, 130, 480))
        self.sidebar.setStyleSheet("background: #253442;")
        self.sidebar.setObjectName("sidebar")

        self.about_btn_widget = QtWidgets.QWidget(self.sidebar)
        self.about_btn_widget.setGeometry(QtCore.QRect(0, 113, 130, 111))
        self.about_btn_widget.setStyleSheet("background: #212c38;")
        self.about_btn_widget.setObjectName("about_btn_widget")

        self.question_image_label = QtWidgets.QLabel(self.about_btn_widget)
        self.question_image_label.setGeometry(QtCore.QRect(30, 10, 80, 70))
        self.question_image_label.setText("")
        self.question_image_label.setPixmap(QtGui.QPixmap("question.png"))
        self.question_image_label.setScaledContents(True)
        self.question_image_label.setObjectName("question_image_label")

        self.about_label_btn = QtWidgets.QLabel(self.about_btn_widget)
        self.about_label_btn.setGeometry(QtCore.QRect(50, 80, 51, 20))
        self.about_label_btn.setObjectName("about_label_btn")

        self.evaluator_btn_widget = QtWidgets.QWidget(self.sidebar)
        self.evaluator_btn_widget.setGeometry(QtCore.QRect(0, 0, 130, 111))
        self.evaluator_btn_widget.setStyleSheet("background: #212c38;")
        self.evaluator_btn_widget.setObjectName("evaluator_btn_widget")

        self.shield_image_label = QtWidgets.QLabel(self.evaluator_btn_widget)
        self.shield_image_label.setGeometry(QtCore.QRect(30, 10, 80, 70))
        self.shield_image_label.setText("")
        self.shield_image_label.setPixmap(QtGui.QPixmap("shield.png"))
        self.shield_image_label.setScaledContents(True)
        self.shield_image_label.setObjectName("shield_image_label")
        
        self.evaluator_label_btn = QtWidgets.QLabel(self.evaluator_btn_widget)
        self.evaluator_label_btn.setGeometry(QtCore.QRect(40, 80, 70, 20))
        self.evaluator_label_btn.setObjectName("evaluator_label_btn")

        self.stackedWidget = QtWidgets.QStackedWidget(USBEvaluatorGui)
        self.stackedWidget.setGeometry(QtCore.QRect(130, 0, 670, 480))
        self.stackedWidget.setObjectName("stackedWidget")

        self.evaluator_page = QtWidgets.QWidget()
        self.evaluator_page.setObjectName("evaluator_page")

        self.logs_text_box = QtWidgets.QPlainTextEdit(self.evaluator_page)
        self.logs_text_box.setGeometry(QtCore.QRect(7, 260, 650, 210))

        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(SMALL_FONT)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.logs_text_box.setFont(font)
        self.logs_text_box.setStyleSheet("font: 10pt;")
        self.logs_text_box.setReadOnly(True)
        self.logs_text_box.setPlainText("")
        self.logs_text_box.setObjectName("logs_text_box")

        self.logs_label = QtWidgets.QLabel(self.evaluator_page)
        self.logs_label.setGeometry(QtCore.QRect(10, 230, 60, 20))
        self.logs_label.setObjectName("logs_label")

        self.toggle_evaluator_btn = QtWidgets.QPushButton(self.evaluator_page)
        self.toggle_evaluator_btn.setGeometry(QtCore.QRect(240, 50, 150, 150))
        
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(LARGE_FONT)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.toggle_evaluator_btn.setFont(font)
        self.toggle_evaluator_btn.setStyleSheet("QPushButton {\n"
            "    font: 14pt;\n"
            "    border: 2px solid green;\n"
            "    border-radius: 75px;\n"
            "    border-style: outset;\n"
            "    background: #34495e;\n"
            "    color: white;\n"
            "    padding: 5px;\n"
            "    }\n"
            "\n"
            "QPushButton:pressed {\n"
            "    border-style: inset;\n"
            "    background: #7ba8d6;\n"
            "    }")
        self.toggle_evaluator_btn.setObjectName("toggle_evaluator_btn")

        self.stackedWidget.addWidget(self.evaluator_page)
        
        self.about_page = QtWidgets.QWidget()
        self.about_page.setObjectName("about_page")
        
        self.stackedWidget.addWidget(self.about_page)

        self.retranslateUi(USBEvaluatorGui)
        self.stackedWidget.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(USBEvaluatorGui)

    def retranslateUi(self, USBEvaluatorGui):
        _translate = QtCore.QCoreApplication.translate
        USBEvaluatorGui.setWindowTitle(_translate("USBEvaluatorGui", "USBEvaluatorGui"))

        self.toggle_evaluator_btn.clicked.connect(self.__toggle_evaluator)

        self.about_label_btn.setText(_translate("USBEvaluatorGui", "About"))
        self.evaluator_label_btn.setText(_translate("USBEvaluatorGui", "Evaluator"))
        self.logs_label.setText(_translate("USBEvaluatorGui", "Logs:"))
        self.toggle_evaluator_btn.setText(_translate("USBEvaluatorGui", "Start"))

    def normal_write_text(self, text):
        cursor = self.logs_text_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)

        self.logs_text_box.setTextCursor(cursor)
        self.logs_text_box.ensureCursorVisible()
    
    def __toggle_evaluator(self):
        if self.is_started:
            print('>>> Stopping evaluator.')
            usb_detector.stop()
        else:
            print('>>> Starting evaluator')
            
            worker = GuiThreadWorker()
            self.threadpool.start(worker)
            self.is_started = True


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

show_gui()


def show_msg_box(box_title, box_content, buttons = 'Okay'):
    alert(box_content, box_title, buttons)

def show_confirm_box(box_title, box_content, displayed_buttons = ['Yes', 'No']):
    result = confirm(text=box_content, title=box_title, buttons=displayed_buttons)
    if result == 'OK':
        return True
    else:
        return False