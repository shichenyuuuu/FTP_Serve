import sys
import PyQt5
from PyQt5.QtWidgets import *
import time
from threading import Thread

class BaseProgressWidget(QWidget):
    updateProgress = PyQt5.QtCore.pyqtSignal([bytes])
    setValues = PyQt5.QtCore.pyqtSignal()
    def __init__(self, text='', parent=None):
        super(BaseProgressWidget, self).__init__(parent)
        self.setFixedHeight(50)
        self.text  = text
        self.progressbar = QProgressBar()
        self.progressbar.setTextVisible(True)

        self.updateProgress.connect(self.set_value)
        self.setValues.connect(self.set_now)

        self.bottomBorder = QWidget()
        self.bottomBorder.setStyleSheet("""
            background: palette(shadow);
        """)
        self.bottomBorder.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.bottomBorder.setMinimumHeight(1)

        self.label  = QLabel(self.text)
        self.label.setStyleSheet("""
            font-weight: bold;
        """)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10,0,10,0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressbar)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addWidget(self.bottomBorder)
        self.setLayout(self.mainLayout)
        self.totalValue = 0
        self.maxValue = 0

    def set_value(self, value):
        self.totalValue += len(value)
        self.progressbar.setValue(self.totalValue)

    def set_now(self):
        self.totalValue = self.maxValue
        self.progressbar.setValue(self.totalValue)

    def set_max(self, value):
        self.progressbar.setMaximum(value)
        self.maxValue = value


class DownloadProgressWidget(BaseProgressWidget):
    def __init__(self, text='Downloading', parent=None):
        super(DownloadProgressWidget, self).__init__(text, parent)
        style ="""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font-color: rgb(255,255,255);
        }

        QProgressBar::chunk {
            background-color: #37DA7E;
            width: 20px;
        }"""
        self.progressbar.setStyleSheet(style)


class UploadProgressWidget(BaseProgressWidget):
    def __init__(self, text='Uploading', parent=None):
        super(UploadProgressWidget, self).__init__(text, parent)
        style ="""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            text-align: center;
            font-color: rgb(255,255,255);
        }

        QProgressBar::chunk {
            background-color: #88B0EB;
            width: 20px;
        }"""
        self.progressbar.setStyleSheet(style)

# class MessageBox(QMessageBox):
#     message_sig = PyQt5.QtCore.pyqtSignal(str)
#     def __init__(self, parent=None):
#         super(MessageBox, self).__init__(parent)
#         self.message_sig.connect(self.inform)
#
#     # def inform(self,message):
#     #     self.information(parent, 'Message', message)