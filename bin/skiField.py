from qgis.core import QgsPointXY
import pandas as pd


class SkiField(object):

    def __init__(self, en_name, location, zh_name=None, city_name="北京"):
        """
        创建一个新的滑雪场对象
        :param en_name: 滑雪场英文名称
        :param location: 滑雪场位置
        :param zh_name: 滑雪场中文名称
        :param city_name: 滑雪场所在城市
        """
        self.en_name = en_name
        self.zh_name = zh_name
        self.location = location
        self.busInfo = self._getBusInfo()

    def _getBusInfo(self):
        """
        获得滑雪场的班车信息
        :return: 一个 (出发地, 出发时间, 出发地经纬度) 的dataframe
        """
        bus_df = pd.read_excel("data/shuttleBus.xlsx")
        return bus_df[bus_df['滑雪场名称'] == self.zh_name]

