import sys
from qgis.PyQt import QtCore
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
from dialogs.myWelcomeWindow import MyWelcomeWindow
import os
import traceback


if __name__ == '__main__':
    os.environ["PROJ_LIB"] = '/Applications/QGIS-LTR.app/Contents/Resources/proj'  # QGIS自带Bug，需要指定路径
    QgsApplication.setPrefixPath('/Applications/QGIS-LTR.app/Contents/MacOS', True)  # 初始化QGIS路径
    # QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 暂时不知道有什么用
    app = QgsApplication([], True)  # 创建一个QgsApplication对象，该对象是QApplication的子类
    app.initQgis()  # 初始化QGIS
    win = MyWelcomeWindow()  # 创建一个自定义的窗口
    win.show()
    sys.exit(app.exec_())
