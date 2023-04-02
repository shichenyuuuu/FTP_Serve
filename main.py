import os
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QInputDialog, QLineEdit,
                             QMessageBox, QTreeWidgetItem, QFileDialog,
                             )


from dialog import *
from ClientGui import Ui_Form
from utils import fileProperty
import ftp_client
from logger import put_text
from logger import logger
from scanner import Scanner

import qdarkstyle

app_icon_path = os.path.join(os.path.dirname(__file__), 'icons')
qIcon = lambda name: QIcon(os.path.join(app_icon_path, name))


def upload_emit(myWin):
    item = myWin.Local_Filelist.currentItem()
    filesize = int(item.text(1))

    try:
        srcfile = os.path.join(myWin.local_pwd, str(item.text(0).toUtf8()))
        dstfile = os.path.join(myWin.pwd, str(item.text(0).toUtf8()))
        dstfile = dstfile.replace('\\', '/')
    except AttributeError:
        srcfile = os.path.join(myWin.local_pwd, str(item.text(0)))
        dstfile = os.path.join(myWin.pwd, str(item.text(0)))
        dstfile = dstfile.replace('\\', '/')

    try:
        origin_len = len(myWin.widgetlist)
        myWin.addProgress_sig.emit('upload', 'Upload ' + srcfile, filesize)
        while origin_len == len(myWin.widgetlist):
            pass

        pb = myWin.widgetlist[len(myWin.widgetlist) - 1]

        ftp_client.uploadFile(myWin.s, srcfile, str(item.text(0)), pb)

        myWin.remotrRefresh_sig.emit(1)
    except Exception as e:
        # message = QMessageBox.information(self,'无权限','对不起，您没有此操作的权限')
        put_text('对不起，您没有此操作的权限。错误原因：{}'.format(str(e)), color="red")


def download_emit(myWin):
    try:
        pb = DownloadProgressWidget(text="a")
        myWin.verticalLayout.addWidget(pb)
        item = myWin.Remote_Filelist.currentItem()
        filesize = int(item.text(1))
    except:
        pass

    try:
        srcfile = os.path.join(myWin.pwd, str(item.text(0).toUtf8()))
        srcfile = srcfile.replace('\\', '/')
        dstfile = os.path.join(myWin.local_pwd, str(item.text(0).toUtf8()))

    except AttributeError:
        srcfile = os.path.join(myWin.pwd, str(item.text(0)))
        srcfile = srcfile.replace('\\', '/')
        dstfile = os.path.join(myWin.local_pwd, str(item.text(0)))

    try:
        origin_len = len(myWin.widgetlist)

        myWin.addProgress_sig.emit('download', 'Download ' + srcfile, filesize)
        while (origin_len == len(myWin.widgetlist)):
            pass

        pb = myWin.widgetlist[len(myWin.widgetlist) - 1]

        ftp_client.getFile(myWin.s, srcfile, dstfile, pb)

    except Exception as e:
        print('下载文件时失败', "noshow")


class MyMainGui(QWidget, Ui_Form):
    addProgress_sig = PyQt5.QtCore.pyqtSignal(str, str, int)
    remotrRefresh_sig = PyQt5.QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MyMainGui, self).__init__(parent)
        self.setupUi(self)
        self.downloads = []
        self.Remote_Home.clicked.connect(self.cdToRemoteHomeDirectory)
        self.Remote_Filelist.itemDoubleClicked.connect(self.cdToRemoteDirectory)
        self.Remote_Return.clicked.connect(self.cdToRemoteBackDirectory)
        self.Remote_Next.clicked.connect(self.cdToRemoteNextDirectory)

        self.Local_Home.clicked.connect(self.cdToLocalHomeDirectory)
        self.Local_Filelist.itemDoubleClicked.connect(self.cdToLocalDirectory)
        self.Local_Return.clicked.connect(self.cdToLocalBackDirectory)
        self.Local_Next.clicked.connect(self.cdToLocalNextDirectory)
        # self.Local_Upload.clicked.connect(lambda: Thread(target=self.upload).start())
        self.passwdEdit.returnPressed.connect(self.connect)
        self.Local_Connect.clicked.connect(self.connect)#建立连接

        # right mouse button menu
        self.Local_Filelist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Local_Filelist.customContextMenuRequested.connect(self.local_right_menu)
        self.Remote_Filelist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Remote_Filelist.customContextMenuRequested.connect(self.remote_right_menu)

        self.registerRadio.clicked.connect(self.register)
        self.visitorRadio.clicked.connect(self.visitor)

        # completer for path edit
        Remote_completer = QCompleter()
        self.Remote_completerModel = QStringListModel()
        Remote_completer.setModel(self.Remote_completerModel)

        self.Remote_path.setCompleter(Remote_completer)#动态显示完成列表
        self.Remote_path.returnPressed.connect(self.cdToRemotePath)#回车

        Local_completer = QCompleter()
        self.Local_completerModel = QStringListModel()
        Local_completer.setModel(self.Local_completerModel)
        self.Local_path.setCompleter(Local_completer)
        self.Local_path.returnPressed.connect(self.cdToLocalPath)

        # set button state by default
        self.Local_Home.setEnabled(False)
        self.Local_Return.setEnabled(False)
        self.Local_Next.setEnabled(False)
        self.local_op = False
        self.Local_file_address.setEnabled(False)#增加

        self.Remote_Home.setEnabled(False)
        self.Remote_Return.setEnabled(False)
        self.Remote_Next.setEnabled(False)
        self.remote_op = False

        self.addProgress_sig.connect(self.addProgress)
        self.remotrRefresh_sig.connect(self.remoteRefresh)
    #修改
    #绑定函数文件夹选择函数
        self.Local_file_address.clicked.connect(self.openFloder)
    #文件下拉框
    def openFloder(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹")  # 起始路径
        self.Local_path.setText(str(directory))
        #self.Local_path.returnPressed.connect(self.cdToLocalPath)

    def _set_current_item(self, list_type, filename):
        file_list = self.Local_Filelist if list_type == 'local' else self.Remote_Filelist
        total_file = file_list.topLevelItemCount()
        for i in range(total_file):
            if (file_list.topLevelItem(i).text(0) == filename):
                file_list.setCurrentItem(file_list.topLevelItem(i))
                break

    def local_right_menu(self, pos):#右键菜单函数
        if self.local_op is False:
            return

        item = self.Local_Filelist.currentItem()
        # item.setFlags(Qt.ItemIsEditable)

        menu = QMenu(self.Local_Filelist)
        refresh = menu.addAction("刷新")
        mkdir = menu.addAction("新建文件夹")
        newfile = menu.addAction("新建文件")
        rename = menu.addAction("重命名")
        if item and item.text(3) == "文件":
            upload = menu.addAction("上传文件")
        remove = menu.addAction("删除文件")
        action = menu.exec_(self.Local_Filelist.mapToGlobal(pos))

        # refresh
        if action == refresh:
            self.updateLocalFileList()#更新本地文件列表
            return

        # mkdir新建文件夹
        elif action == mkdir:
            try:
                dir_name = QInputDialog.getText(self, '创建文件夹', '请输出文件夹名称', QLineEdit.Normal)
                if not dir_name[1]:
                    return
                # os.mkdir(os.path.join(self.local_pwd, dir_name[0]))
                os.mkdir(self.local_pwd + './' + dir_name[0])
                self.updateLocalFileList()
                self._set_current_item('local', dir_name[0])

            except FileExistsError:
                message = QMessageBox.information(self, '文件夹已存在', '文件夹名称已存在，请修改文件名称后再创建')

        # remove #删除文件
        elif action == remove:

            topCount = self.Local_Filelist.topLevelItemCount()
            for i in range(topCount):
                item_chosen = self.Local_Filelist.topLevelItem(i)
                if (item_chosen == item):
                    break

            import shutil
            pathname = os.path.join(self.local_pwd, str(item.text(0)))
            # pathname = pathname.replace('\\', '/')
            if (os.path.isdir(pathname)):
                shutil.rmtree(pathname)
            else:
                os.remove(pathname)
            self.updateLocalFileList()
            self.Local_Filelist.setCurrentItem(self.Local_Filelist.topLevelItem(i))

        # rename
        elif action == rename:
            rename = QInputDialog.getText(self, '重命名', '请输出文件名', QLineEdit.Normal)
            if not rename[1]:
                return
            pathname = os.path.join(self.local_pwd, str(item.text(0)))
            # pathname = pathname.replace('\\', '/')
            os.rename(pathname, os.path.join(self.local_pwd, str(rename[0])))
            self.updateLocalFileList()
            self._set_current_item('local', rename[0])

        # new file
        elif action == newfile:
            file_name = QInputDialog.getText(self, '创建文件', '请输出文件名', QLineEdit.Normal)
            if not file_name[1]:
                return
            try:
                open(self.local_pwd + './' + file_name[0], mode='x')
                import webbrowser
                webbrowser.open(self.local_pwd + './' + file_name[0])
                self.updateLocalFileList()
                self._set_current_item('local', file_name[0])

            except FileExistsError:#弹出提示框
                message = QMessageBox.information(self, '文件已存在', '文件名已存在，请重新创建')
        elif item.text(3) == "文件" and action == upload:
            try:
                self.upload()
            except:
                put_text('上传失败', 'noshow')
        else:
            return

    def remote_right_menu(self, pos):#远程右键菜单
        if self.remote_op is False:
            return
        item = self.Remote_Filelist.currentItem()
        # item.setFlags(Qt.ItemIsEditable)
        menu = QMenu(self.Remote_Filelist)
        refresh = menu.addAction("刷新")
        if item:
            if item.text(3) == "文件":
                download = menu.addAction("下载文件")
                removefile = menu.addAction("删除文件")
            else:
                removedir = menu.addAction("删除文件夹")
        mkdir = menu.addAction("新建文件夹")

        action = menu.exec_(self.Remote_Filelist.mapToGlobal(pos))

        try:
            if action == refresh:
                self.updateRemoteFileList()
                return

            elif item.text(3) == "文件" and action == download:
                self.download()
            elif item.text(3) == "文件" and action == removefile:
                self.removeFile()
            elif action == mkdir:
                self.makeDIR()
            elif action == removedir:
                self.removeDIR()
            else:
                pass
        except:
            pass

    def initialize(self):#初始化函数
        self.localBrowseRec = []
        self.remoteBrowseRec = []
        self.pwd = "/"
        self.local_pwd = os.getenv('HOME') if os.name == 'posix' else 'D:\\'
        self.remoteOriginPath = self.pwd
        self.localOriginPath = self.local_pwd
        self.localBrowseRec.append(self.local_pwd)
        self.downloadToRemoteFileList()
        self.loadToLocaFileList()
        # set button state by default
        self.Local_file_address.setEnabled(True)  # 增加
        self.local_op = True
        self.remote_op = True
        self.Local_path.setText(self.local_pwd)
        self.Remote_path.setText(self.pwd)
        self.Remote_label.setText("{}:{}".format(self.host, str(self.port)))
        self.widgetlist = []
        _, self.pwd = ftp_client.getPwd(self.s)
        self.remoteBrowseRec.append(self.pwd)

    def register(self):#登录
        self.nameEdit.setEnabled(True)
        self.passwdEdit.setEnabled(True)

    def visitor(self):#匿名访问
        self.nameEdit.setEnabled(False)
        self.passwdEdit.setEnabled(False)

    def connect(self):#连接函数
        put_text('FTP > 正在尝试进行连接', color="blue")#尝试改颜色
        try:
            from urlparse import urlparse
        except ImportError:
            from urllib.parse import urlparse

        result = str(self.hostEdit.text())#hostEdit是主机栏的输入框
        host = str(result)

        try:
            self.s = ftp_client.client(host, 21)
            self.host = host
            self.port = 21#端口号21
            self.login()#调用登录函数
        except Exception as e:
            put_text(str(e), color="red")
            message = QMessageBox.warning(self, '地址错误', '连接主机时发生异常')

    def login(self):#登录函数
        ask = ()
        if self.visitorRadio.isChecked():#匿名访问被选择（可删除）
            ask = ('Anonymous', '', True)#信息匿名
        else:#获取登录信息的字符串
            ask = (str(self.nameEdit.text()), str(self.passwdEdit.text()), True)

        user, passwd = ask[:2]#赋值
        put_text(user + " " + passwd, "noshow")#passwd不显示
        try:
            ftp_client.ftp_login(self.s, user, passwd)#调用
            message = QMessageBox.information(self, '登陆成功', '已连接服务器')
            self.initialize()#进行初始化
        except Exception as e:
            message = QMessageBox.information(self, '登陆错误', '账号密码错误，请重新输入')
            put_text(str(e), color="red")

    def downloadToRemoteFileList(self):
        """
        download file and directory list from FTP Server
        """
        self.remoteWordList = []
        self.remoteDir = {}
        content = ftp_client.listDir(self.s)
        files = content.split("\r\n")
        for singel in files:
            if singel:
                self.addItemToRemoteFileList(singel)
        self.Remote_completerModel.setStringList(self.remoteWordList)

    def addItemToRemoteFileList(self, content):
        mode, num, owner, group, size, date, filename = self.parseFileInfo(content)
        filetype = "文件"
        if content.startswith('d'):
            icon = qIcon('folder.png')
            pathname = os.path.join(self.pwd, filename)
            pathname = pathname.replace('\\', '/')
            self.remoteDir[pathname] = True
            self.remoteWordList.append(filename)
            filetype = "目录"
        else:
            icon = qIcon('file.png')
            filetype = "文件"

        item = QTreeWidgetItem()
        item.setIcon(0, icon)
        for n, i in enumerate((filename, size, date, filetype)):
            item.setText(n, i)

        self.Remote_Filelist.addTopLevelItem(item)
        if not self.Remote_Filelist.currentItem():
            self.Remote_Filelist.setCurrentItem(self.Remote_Filelist.topLevelItem(0))
            self.Remote_Filelist.setEnabled(True)

    def parseFileInfo(self, file):
        """
        parse files information "drwxr-xr-x 2 root wheel 1024 Nov 17 1993 lib" result like follower
                                "drwxr-xr-x", "2", "root", "wheel", "1024", "Nov 17 1993", "lib"
        """
        # FileMode, FilesNumber, User, Group, Size, Date, Filename
        item = [f for f in file.split(' ') if f != '']
        # if windows, item = ftype, num, size, date, filename
        # if linux, item = mode,num,owner,group,size,date,filename

        if item[0] == 'folder' or item[0] == 'file':  # windows
            ftype, num, size, date, filename = (item[0], item[1], item[2], ' '.join(item[3:6]), ' '.join(item[6:]))
            return (ftype, num, size, date, filename)

        else:  # linux
            while len(item) < 8:
                item.append(" ")
            mode, num, owner, group, size, date, filename = (
                item[0], item[1], item[2], item[3], item[4], ' '.join(item[5:8]), ' '.join(item[8:]))
            if filename.replace(" ", "") == "":
                filename = ".."
            return (mode, num, owner, group, size, date, filename)

    def loadToLocaFileList(self):
        """
        load file and directory list from local computer
        """
        self.localWordList = []
        self.localDir = {}
        for f in os.listdir(self.local_pwd):
            pathname = os.path.join(self.local_pwd, f)
            self.addItemToLocalFileList(fileProperty(pathname))
        self.Local_completerModel.setStringList(self.localWordList)

    def addItemToLocalFileList(self, content):

        # mode, num, owner, group, size, date, filename = self.parseFileInfo(content)
        ftype, num, size, date, filename = self.parseFileInfo(content)
        filetype = "文件"
        if ftype == 'folder':
            icon = qIcon('folder.png')
            pathname = os.path.join(self.local_pwd, filename)
            self.localDir[pathname] = True
            self.localWordList.append(filename)
            filetype = "目录"
        else:
            icon = qIcon('file.png')
            filetype = "文件"

        item = QTreeWidgetItem()
        item.setIcon(0, icon)
        for n, i in enumerate((filename, size, date, filetype)):
            # print((filename, size, owner, group, date, mode))
            item.setText(n, i)
        self.Local_Filelist.addTopLevelItem(item)
        if not self.Local_Filelist.currentItem():
            self.Local_Filelist.setCurrentItem(self.Local_Filelist.topLevelItem(0))
            self.Local_Filelist.setEnabled(True)

    def cdToRemotePath(self):
        try:
            pathname = str(self.Remote_path.text().toUtf8())
        except AttributeError:
            pathname = str(self.Remote_path.text())
        try:
            ftp_client.changeWorkingDir(self.s, pathname)
        except:
            return

        if self.remoteBrowseRec[self.remoteBrowseRec.index(self.pwd)]:
            self.remoteBrowseRec = self.remoteBrowseRec[:self.remoteBrowseRec.index(self.pwd) + 1]

        self.pwd = pathname.startswith(os.path.sep) and pathname or os.path.join(self.pwd, pathname)
        self.pwd = self.pwd.replace('\\', '/')
        self.updateRemoteFileList()
        self.Remote_Return.setEnabled(True)

        self.remoteBrowseRec.append(self.pwd)

        if os.path.abspath(pathname) != self.remoteOriginPath:
            self.Remote_Home.setEnabled(True)
        else:
            self.Remote_Home.setEnabled(False)
        self.Remote_Next.setEnabled(False)

    def cdToRemoteDirectory(self, item, column):
        if str(item.text(0)) == "..":
            self.cdToRemoteBackDirectory()
            return
        if self.remoteBrowseRec[self.remoteBrowseRec.index(self.pwd)]:
            self.remoteBrowseRec = self.remoteBrowseRec[:self.remoteBrowseRec.index(self.pwd) + 1]
        pathname = os.path.join(self.pwd, str(item.text(0)))
        pathname = pathname.replace('\\', '/')
        # print(pathname)
        if not item.text(3) == "目录":
            put_text("{}不是一个正确的目录".format(pathname))
            return
        self.remoteBrowseRec.append(pathname)
        ftp_client.changeWorkingDir(self.s, pathname)
        self.pwd = pathname
        self.updateRemoteFileList()
        self.Remote_Return.setEnabled(True)
        if pathname != self.remoteOriginPath:
            self.Remote_Home.setEnabled(True)
        self.Remote_Next.setEnabled(False)

    def cdToRemoteBackDirectory(self):
        pathname = self.remoteBrowseRec[self.remoteBrowseRec.index(self.pwd) - 1]
        if pathname != self.remoteBrowseRec[0]:
            self.Remote_Return.setEnabled(True)
        else:
            self.Remote_Return.setEnabled(False)

        if pathname != self.remoteOriginPath:
            self.Remote_Home.setEnabled(True)
        else:
            self.Remote_Home.setEnabled(False)
        self.Remote_Next.setEnabled(True)
        self.pwd = pathname
        ftp_client.changeWorkingDir(self.s, pathname)
        self.updateRemoteFileList()

    def cdToRemoteNextDirectory(self):  # Trigger condition:Click → Button
        pathname = self.remoteBrowseRec[self.remoteBrowseRec.index(self.pwd) + 1]
        if pathname != self.remoteBrowseRec[-1]:
            self.Remote_Next.setEnabled(True)
        else:
            self.Remote_Next.setEnabled(False)
        if pathname != self.remoteOriginPath:
            self.Remote_Home.setEnabled(True)
        else:
            self.Remote_Home.setEnabled(False)
        self.Remote_Return.setEnabled(True)
        self.pwd = pathname
        ftp_client.changeWorkingDir(self.s, pathname)
        self.updateRemoteFileList()

    def cdToRemoteHomeDirectory(self):
        ftp_client.changeWorkingDir(self.s, self.remoteOriginPath)
        self.pwd = self.remoteOriginPath
        self.updateRemoteFileList()
        self.Remote_Home.setEnabled(False)
        self.Remote_Return.setEnabled(False)

    def cdToLocalPath(self):
        try:
            pathname = str(self.Local_path.text().toUtf8())
        except AttributeError:
            pathname = str(self.Local_path.text())
        pathname = pathname.startswith(os.path.sep) and pathname or os.path.join(self.local_pwd, pathname)
        if not os.path.exists(pathname) and not os.path.isdir(pathname):
            return
        else:
            if self.localBrowseRec[self.localBrowseRec.index(self.local_pwd)]:
                self.localBrowseRec = self.localBrowseRec[:self.localBrowseRec.index(self.local_pwd) + 1]
            self.localBrowseRec.append(pathname)
            self.local_pwd = pathname
            self.updateLocalFileList()
            self.Local_Return.setEnabled(True)
            # print(pathname, self.localOriginPath)
            if os.path.abspath(pathname) != self.localOriginPath:
                self.Local_Home.setEnabled(True)
            else:
                self.Local_Home.setEnabled(False)
            self.Local_Next.setEnabled(False)

    def cdToLocalDirectory(self, item, column):
        if self.localBrowseRec[self.localBrowseRec.index(self.local_pwd)]:
            self.localBrowseRec = self.localBrowseRec[:self.localBrowseRec.index(self.local_pwd) + 1]
        pathname = os.path.join(self.local_pwd, str(item.text(0)))
        if not self.isLocalDir(pathname):
            return
        self.localBrowseRec.append(pathname)
        # print(self.localBrowseRec)
        self.local_pwd = pathname
        self.updateLocalFileList()
        self.Local_Return.setEnabled(True)
        if pathname != self.localOriginPath:
            self.Local_Home.setEnabled(True)
        self.Local_Next.setEnabled(False)

    def cdToLocalBackDirectory(self):
        pathname = self.localBrowseRec[self.localBrowseRec.index(self.local_pwd) - 1]
        # print(self.localBrowseRec)
        # print(self.local_pwd)
        if pathname != self.localBrowseRec[0]:
            self.Local_Return.setEnabled(True)
        else:
            self.Local_Return.setEnabled(False)
        if pathname != self.localOriginPath:
            self.Local_Home.setEnabled(True)
        else:
            self.Local_Home.setEnabled(False)
        self.Local_Next.setEnabled(True)
        self.local_pwd = pathname
        self.updateLocalFileList()

    def cdToLocalNextDirectory(self):
        pathname = self.localBrowseRec[self.localBrowseRec.index(self.local_pwd) + 1]
        # print(self.localBrowseRec)
        # print(self.local_pwd)
        if pathname != self.localBrowseRec[-1]:
            self.Local_Next.setEnabled(True)
        else:
            self.Local_Next.setEnabled(False)
        if pathname != self.localOriginPath:
            self.Local_Home.setEnabled(True)
        else:
            self.Local_Home.setEnabled(False)
        self.Local_Return.setEnabled(True)
        self.local_pwd = pathname
        self.updateLocalFileList()

    def cdToLocalHomeDirectory(self):
        self.local_pwd = self.localOriginPath
        self.updateLocalFileList()
        self.Local_Home.setEnabled(False)
        self.Local_Return.setEnabled(False)

    def updateLocalFileList(self):
        self.Local_Filelist.clear()
        self.loadToLocaFileList()

        self.Local_path.setText(self.local_pwd)

    def updateRemoteFileList(self):
        self.Remote_Filelist.clear()
        self.downloadToRemoteFileList()

        self.Remote_path.setText(self.pwd)

    def isLocalDir(self, dirname):
        return self.localDir.get(dirname, None)

    def isRemoteDir(self, dirname):
        return self.remoteDir.get(dirname, None)

    def remoteRefresh(self, int):
        if int == 1:
            self.updateRemoteFileList()

    def addProgressbar(self, progressbar):
        self.verticalLayout.addWidget(progressbar)

    def addProgress(self, type, title, size):
        if type not in ['download', 'upload']:
            raise ("发生下载上传错误")

        if type == 'download':
            pb = DownloadProgressWidget(text=title)
        else:
            pb = UploadProgressWidget(text=title)
        pb.set_max(size)
        self.verticalLayout.addWidget(pb)
        self.widgetlist.append(pb)
        print('已添加新的下载进程')
        # print(len(self.widgetlist))

    def download(self):
        dl = Thread(target=download_emit, args=(self,))
        dl.start()

    def upload(self):
        ul = Thread(target=upload_emit, args=(self,))
        ul.start()

    def removeDIR(self):
        item = self.Remote_Filelist.currentItem()

        try:
            dstdir = os.path.join(self.pwd, str(item.text(0).toUtf8()))
            dstdir = dstdir.replace('\\', '/')
        except AttributeError:
            dstdir = os.path.join(self.pwd, str(item.text(0)))
            dstdir = dstdir.replace('\\', '/')

        try:
            ftp_client.removeDir(self.s, dstdir)
            self.updateRemoteFileList()
        except:
            message = QMessageBox.warning(self, '删除失败！', '无法删除当前文件夹')

    def removeFile(self):
        item = self.Remote_Filelist.currentItem()
        filesize = int(item.text(1))

        try:
            dstfile = os.path.join(self.pwd, str(item.text(0).toUtf8()))
            dstfile = dstfile.replace('\\', '/')
        except AttributeError:
            dstfile = os.path.join(self.pwd, str(item.text(0)))
            dstfile = dstfile.replace('\\', '/')

        try:
            ftp_client.deleteFile(self.s, dstfile)
            self.updateRemoteFileList()
        except:
            message = QMessageBox.warning(self, '删除失败！', '无法删除当前文件')

    def makeDIR(self):
        dir_name = QInputDialog.getText(self, '创建文件夹', '请输出文件夹名称', QLineEdit.Normal)
        if not dir_name[1]:
            return
        dstdir = os.path.join(self.pwd, str(dir_name[0]))
        dstdir = dstdir.replace('\\', '/')

        try:
            ftp_client.makeDir(self.s, dstdir)
            self.updateRemoteFileList()
            self._set_current_item('remote', dir_name[0])
        except:
            message = QMessageBox.warning(self, '删除失败！', '无法删除当前文件')


class ScannerGui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.listwidget = QListWidget(self)  # 实例化列表控件
        self.listwidget.doubleClicked.connect(self.choose_ip)


        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        self.btn = QPushButton('开始扫描', self)
        self.btn.clicked.connect(self.doScan)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(30, 30, 30, 30)
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.listwidget)
        vbox.addWidget(self.btn)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('扫描当前局域网')
        self.setLayout(vbox)
        self.show()

    def doScan(self):
        '''开始扫描局域网'''
        threading.Thread(target=Scanner.run).run()
        while True:
            value = Scanner.get_progress()
            self.pbar.setValue(value)
            if value == 100:
                break
        self.listwidget.addItems(Scanner.ip_list)  # 添加项目-列表

    def choose_ip(self):
        ip=self.listwidget.currentItem().text()
        self.hide()
        myWin.show()
        myWin.hostEdit.setText(ip)

app = QApplication(sys.argv)
myWin = MyMainGui()
logger.setmyWin(myWin)
#app.setStyleSheet(qdarkstyle.load_stylesheet())#修改整体颜色样式

sc = ScannerGui()
sys.exit(app.exec_())
