from ui.welcomeWindow import Ui_welcomeDialog
from qgis.PyQt.QtWidgets import QDialog
from myMainWindow import MyMainWindow


class MyWelcomeWindow(QDialog, Ui_welcomeDialog):
    def __init__(self):
        super(MyWelcomeWindow, self).__init__()
        self.setupUi(self)  # 初始化UI和成员变量
        self.enterButton.clicked.connect(self.intoMainWindow)  # 将按钮所对应的函数连接起来
        self.exitButton.clicked.connect(self.exit)

    def intoMainWindow(self):
        self.myMainWindow = MyMainWindow()
        self.myMainWindow.show()  # 显示主窗口
        self.close()  # 关闭自身

    def exit(self):
        super().accept()
