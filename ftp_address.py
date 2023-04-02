import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
    # 创建打开文件夹按钮
        self.openFolderBtn = QPushButton('打开文件夹', self)
        self.openFolderBtn.clicked.connect(self.openFolder)
        # 创建路径标签
        self.pathLabel = QLabel('请选择文件夹', self)
        # 创建垂直布局器
        vbox = QVBoxLayout()
        vbox.addWidget(self.openFolderBtn)
        vbox.addWidget(self.pathLabel)
    # 设置主窗口布局
        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('文件夹选择')
        self.show()
    def openFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, '选择文件夹')
        self.pathLabel.setText(folderPath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())