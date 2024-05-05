from qgis.core import QgsPoint, QgsCoordinateTransform, QgsCoordinateReferenceSystem, QgsProject, QgsPointXY


def transform4to3(point: QgsPoint):
    """
    一个辅助方法，负责将4326坐标系下的地理坐标换成3857投影坐标
    :param point:
    :return:
    """
    transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"),
                                       QgsCoordinateReferenceSystem("EPSG:3857"), QgsProject.instance())
    old = QgsPointXY(point.x(), point.y())
    new = transform.transform(old)
    return QgsPoint(new.x(), new.y())
