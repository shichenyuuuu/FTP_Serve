from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtGui import QIcon
import os

from PyQt5.QtWidgets import QMainWindow

if getattr(sys, 'frozen', False):
 cur_path = sys._MEIPASS
else:
 cur_path = os.path.dirname(__file__)
print(cur_path)
app_icon_path = os.path.join(cur_path, 'icons')
qIcon = lambda name: QIcon(os.path.join(app_icon_path, name))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 1000)




        self.hostlabel = QtWidgets.QLabel(Form)
        self.hostlabel.setGeometry(QtCore.QRect(20, 16, 72, 30))
        self.hostlabel.setObjectName("hostlabel")
        self.hostEdit = QtWidgets.QLineEdit(Form)
        self.hostEdit.setGeometry(QtCore.QRect(60, 20, 181, 21))
        self.hostEdit.setObjectName("hostEdit")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(250, 16, 72, 30))
        self.label.setObjectName("label")
        self.nameEdit = QtWidgets.QLineEdit(Form)
        self.nameEdit.setGeometry(QtCore.QRect(305, 20, 181, 21))
        self.nameEdit.setObjectName("nameEdit")

        self.passwdLabel = QtWidgets.QLabel(Form)
        self.passwdLabel.setGeometry(QtCore.QRect(490, 16, 72, 30))
        self.passwdLabel.setObjectName("passwdLabel")
        self.passwdEdit = QtWidgets.QLineEdit(Form)
        self.passwdEdit.setGeometry(QtCore.QRect(535, 20, 181, 21))
        self.passwdEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwdEdit.setObjectName("passwdEdit")

        self.registerRadio = QtWidgets.QRadioButton(Form)
        self.registerRadio.setGeometry(QtCore.QRect(820, 22, 91, 25))
        self.registerRadio.setChecked(True)
        self.registerRadio.setObjectName("registerRadio")
        self.visitorRadio = QtWidgets.QRadioButton(Form)
        self.visitorRadio.setGeometry(QtCore.QRect(890, 22,91, 25))
        self.visitorRadio.setObjectName("visitorRadio")

        self.Local_label = QtWidgets.QLabel(Form)
        self.Local_label.setObjectName("Local_label")
        self.Local_label.setGeometry(QtCore.QRect(20, 145, 100, 50))
        self.Remote_label = QtWidgets.QLabel(Form)
        self.Remote_label.setObjectName("Remote_label")
        self.Remote_label.setGeometry(QtCore.QRect(560, 145, 150, 50))
        self.Local_Return = QtWidgets.QPushButton(Form)
        self.Local_Return.setObjectName("Local_Return")
        self.Local_Return.setGeometry(QtCore.QRect(80, 190, 50, 30))
        self.Remote_Return = QtWidgets.QPushButton(Form)
        self.Remote_Return.setObjectName("Remote_Return")
        self.Remote_Return.setGeometry(QtCore.QRect(620, 190, 50, 30))
        self.Remote_Filelist = QtWidgets.QTreeWidget(Form)
        self.Remote_Filelist.setObjectName("Remote_Filelist")
        self.Remote_Filelist.setGeometry(QtCore.QRect(560, 225, 520, 600))
        self.Local_Filelist = QtWidgets.QTreeWidget(Form)
        self.Local_Filelist.setObjectName("Local_Filelist")
        self.Local_Filelist.setGeometry(QtCore.QRect(20, 225, 520, 600))
        self.Local_Next = QtWidgets.QPushButton(Form)
        self.Local_Next.setObjectName("Local_Next")
        self.Local_Next.setGeometry(QtCore.QRect(140, 190, 50, 30))
        self.Local_Home = QtWidgets.QPushButton(Form)
        self.Local_Home.setObjectName("Local_Home")
        self.Local_Home.setGeometry(QtCore.QRect(20, 190, 50, 30))
        self.Local_Connect = QtWidgets.QPushButton(Form)
        self.Local_Connect.setObjectName("Local_Connect")
        self.Local_Connect.setGeometry(QtCore.QRect(720, 15, 80, 30))
        self.Local_path = QtWidgets.QLineEdit(Form)
        self.Local_path.setObjectName("Local_path")
        self.Local_path.setGeometry(QtCore.QRect(200, 190, 340, 30))
        self.Remote_Home = QtWidgets.QPushButton(Form)
        self.Remote_Home.setObjectName("Remote_Home")
        self.Remote_Home.setGeometry(QtCore.QRect(560, 190, 50, 30))
        self.Remote_Next = QtWidgets.QPushButton(Form)
        self.Remote_Next.setObjectName("Remote_Next")
        self.Remote_Next.setGeometry(QtCore.QRect(680, 190, 50, 30))
        self.Remote_path = QtWidgets.QLineEdit(Form)
        self.Remote_path.setObjectName("Remote_path")
        self.Remote_path.setGeometry(QtCore.QRect(740, 190, 340, 30))

        self.logEdit = QtWidgets.QPlainTextEdit(Form)
        self.logEdit.setGeometry(QtCore.QRect(20, 52, 1060, 100))
        self.logEdit.setObjectName("logEdit")
        self.logEdit.isReadOnly()

        self.downlabel = QtWidgets.QLabel(Form)
        self.downlabel.setGeometry(QtCore.QRect(20, 832, 90, 30))
        self.downlabel.setObjectName("downlabel")

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 855, 1060, 150))
        self.widget.setObjectName("widget")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1060, 120))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 100, 50))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        '''self.progressDialog.setGeometry(QtCore.QRect(20, 835, 1000, 1000))
        pb = DownloadProgressWidget(text="hello")
        self.progressDialog.show_sig.emit(1)
        self.progressDialog.addProgress_sig.emit('download', 'Download ', 1024)'''

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.Local_Home.setIcon(qIcon('home.png'))
        self.Local_Next.setIcon(qIcon('next.png'))
        self.Local_Connect.setIcon(qIcon('connect.png'))
        self.Local_Return.setIcon(qIcon('back.png'))

        self.Remote_Next.setIcon(qIcon('next.png'))
        self.Remote_Return.setIcon(qIcon('back.png'))
        self.Remote_Home.setIcon(qIcon('home.png'))


        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "局域网P2P文件传输"))
        self.Local_label.setText(_translate("Form", "本机"))
        self.Remote_label.setText(_translate("Form", "远程服务器"))
        self.downlabel.setText(_translate("Form", "下载/上传"))
        # self.Local_Return.setText(_translate("Form", "←"))
        # self.Remote_Return.setText(_translate("Form", "←"))
        self.hostlabel.setText(_translate("Form", "主机"))
        self.label.setText(_translate("Form", "用户名"))
        self.passwdLabel.setText(_translate("Form", "密码"))
        self.registerRadio.setText(_translate("Form", "登录"))
        self.visitorRadio.setText(_translate("Form", "匿名访问"))
        self.Remote_Filelist.headerItem().setText(0, _translate("Form", "文件名"))
        self.Remote_Filelist.headerItem().setText(1, _translate("Form", "大小"))
        self.Remote_Filelist.headerItem().setText(2, _translate("Form", "修改日期"))
        self.Remote_Filelist.headerItem().setText(3, _translate("Form", "文件类型"))
        self.Local_Filelist.headerItem().setText(0, _translate("Form", "文件名"))
        self.Local_Filelist.headerItem().setText(1, _translate("Form", "大小"))
        self.Local_Filelist.headerItem().setText(2, _translate("Form", "修改日期"))
        self.Local_Filelist.headerItem().setText(3, _translate("Form", "文件类型"))
        # self.Local_Next.setText(_translate("Form", "→"))
        # self.Local_Home.setText(_translate("Form", "Home"))
        self.Local_Connect.setText(_translate("Form", "连接"))
        # self.Remote_Home.setText(_translate("Form", "Home"))
        # self.Remote_Next.setText(_translate("Form", "→"))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

