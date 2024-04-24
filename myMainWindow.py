from ui.mainWindow import Ui_MainWindow
from qgis.gui import *
from qgis.PyQt.QtCore import Qt
from PyQt5.QtWidgets import *
from qgis.core import QgsMapLayer, QgsRasterLayer, QgsVectorLayer, QgsProject, QgsRectangle
from qgisUtils import *
import yaml


class MyMainWindow(Ui_MainWindow, QMainWindow):
    """
    自定义主窗口界面，分别继承了Ui文件和窗口类，其中Ui类主要更改其元素的风格（大小位置等），
    窗口类负责在启动app时呼叫启动函数。
    """
    def __init__(self):
        # 以下是ui文件自生成的风格
        super(MyMainWindow, self).__init__()
        self.setupUi(self)  # 初始化UI和成员变量
        # 以下是QGIS定义的部分
        self.firstAdd = True  # 定义是否第一次加入变量
        self.mapCanvas = QgsMapCanvas(self)  # 创建一个主要的地图的容器，即画布
        self.mapCanvas.setCanvasColor(Qt.white)
        hl = QHBoxLayout(self.frame)  # 创建一个水平布局对象
        hl.addWidget(self.mapCanvas)  # 以水平布局加入主要地图画布

        # self.skiFields =
        # TODO: 完善读取SkiField的代码

        self.addMainMap()
        initial_extent = QgsRectangle(12724169, 4740836, 13103201, 5063319)  # 设置地图初始显示的范围，这里默认为北京市
        self.mapCanvas.setExtent(initial_extent)

        self.actionZoomIn = QAction("放大", self)
        self.actionZoomOut = QAction("缩小", self)
        self.actionPan = QAction("移动", self)

        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut.setCheckable(True)
        self.actionPan.setCheckable(True)

        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.pan)

        self.toolbar = self.addToolBar("Canvas actions")
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionPan)
        # create the map tools
        self.toolPan = QgsMapToolPan(self.mapCanvas)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn = QgsMapToolZoom(self.mapCanvas, False)  # false = in
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.mapCanvas, True)  # true = out
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.pan()

    def zoomIn(self):
        self.mapCanvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.mapCanvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.mapCanvas.setMapTool(self.toolPan)

    def addMainMap(self):
        tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&crs=EPSG3857'
        layer = QgsRasterLayer(tms, 'OSM', 'wms')
        addMapLayer(layer, self.mapCanvas, self.firstAdd)
        self.firstAdd = False

    def getSkiFieldList(self):
        """
        生成一个滑雪场的列表
        :return: a list of SkiFields
        """
        with open('data/attributes.yaml', 'r') as file:
            data = yaml.safe_load(file)
        ski_en_names = data["ski_en_names"]
