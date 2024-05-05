from ui.mainWindow import Ui_MainWindow
from qgis.gui import *
from qgis.PyQt.QtCore import Qt
from PyQt5.QtWidgets import *
from qgis.core import (
    QgsRasterLayer,
    QgsProject,
    QgsRectangle,
    QgsCoordinateReferenceSystem,
    QgsAnnotationLayer,
    QgsAnnotationMarkerItem,
    QgsPoint,
    QgsMarkerSymbol
)
from qgisUtils import *
from bin import *
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

        self.skiFields = self.getSkiFieldList()  # 生成一个多雪场类
        self.addMainMap()

        self.addSkiLayers()  # 将这些雪场添加到图层中
        self.addAnnotations()  # 添加注记
        initial_extent = QgsRectangle(12724169, 4740836, 13103201, 5063319)  # 设置地图初始显示的范围，这里默认为北京市
        self.mapCanvas.setExtent(initial_extent)

        """
        # debug
        self.addSkiLayer("Nanshan")
        self.addSkiLayer("Wanlong")
        nanshan = readVectorFile("data/Track/{0}Track.shp".format("Nanshan"))
        wanlong = readVectorFile("data/Track/{0}Track.shp".format("Wanlong"))
        print(self.mapCanvas.layers())
        """

        """
        PROJECT = QgsProject.instance()
        root = PROJECT.layerTreeRoot()
        osm_layer = PROJECT.mapLayersByName("OSM")[0]
        osm_tree_layer = root.findLayer(osm_layer.id())
        osm_clone = osm_tree_layer.clone()
        root.insertChildNode(-1, osm_clone)
        root.removeChildNode(osm_tree_layer)
        """

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
        tms = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        layer = QgsRasterLayer(tms, 'ZOSM', 'wms')
        addMapLayer(layer, self.mapCanvas, self.firstAdd)
        self.firstAdd = False

    def getSkiFieldList(self):
        """
        生成一个多滑雪场对象
        :return: a list of SkiField
        """
        rSkiList = []
        with open('data/attributes.yaml', 'r') as file:
            data = yaml.safe_load(file)
        ski_en_names = data["ski_en_names"]
        vec_loc = readVectorFile("data/Location/Location.shp")
        name_to_loc = {}  # 将滑雪场英文名和滑雪场的位置信息对应起来的临时字典
        for point in vec_loc.getFeatures():  # 获取所有的Features
            p_geo = point.geometry().asPoint()  # 提取点的坐标信息
            idx = point.fieldNameIndex("Name")
            p_name = point.attributes()[idx]  # 提取点的名字信息
            name_to_loc[p_name] = p_geo
        for en_name in ski_en_names:
            rField = name_to_loc[en_name]  # 找到滑雪场的坐标信息
            rPoint = transform4to3(QgsPoint(rField[0], rField[1]))  # 将其转化为点
            rSkiList.append(SkiField(en_name, rPoint))
        return SkiFields(rSkiList)

    def addSkiLayers(self):
        for field in self.skiFields.skiFields:
            self.addSkiLayer(field.en_name)

    def addSkiLayer(self, en_name):
        vec_track = readVectorFile("data/Track/{0}Track.shp".format(en_name))
        vec_cable = readVectorFile("data/Cablecar/{0}Cable.shp".format(en_name))
        crs = QgsCoordinateReferenceSystem("epsg:4326")
        vec_track.setCrs(crs)
        vec_cable.setCrs(crs)
        addMapLayer(vec_track, self.mapCanvas, self.firstAdd)
        self.firstAdd = False
        addMapLayer(vec_cable, self.mapCanvas, self.firstAdd)

    def addAnnotations(self):
        """
        添加地图上所有的注记
        :return:
        """
        notelayer = QgsAnnotationLayer('Annotations',
                                       QgsAnnotationLayer.LayerOptions(QgsProject.instance().transformContext()))
        for field in self.skiFields.skiFields:
            mark = QgsAnnotationMarkerItem(field.location)
            mark.create()
            notelayer.addItem(mark)
        addMapLayer(notelayer, self.mapCanvas, self.firstAdd)

