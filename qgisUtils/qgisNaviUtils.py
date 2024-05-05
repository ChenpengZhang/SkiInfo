from qgis.core import QgsPointXY
import requests as re
import pandas as pd

KEY = "d1360ddd47decbebd8d5057497d3c79e"


def giveBusRoute(start_location, end_location):
    """
    根据指定的出发位置给出一个乘坐巴士的路线
    :param start_location: 用户指定的出发位置
    :param end_location: 用户指定的结束位置
    :return:
    """
    url = "https://restapi.amap.com/v3/direction/driving"  # 高德地图驾车导航api
    params = {
        "key": KEY,
        "origin": "",  # 经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。格式为x1,y1|x2,y2|x3,y3
        "destination": "",  # 经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
    }
    re.get(url, params=params)


def geoCode(name, city_name):
    """
    高德地图地理编码
    :param name: 地理地点名称
    :param city_name: 城市名
    :return: 一组经纬度信息
    """
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": KEY,
        "address": name,
        "city": city_name
    }
    response = re.get(url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取响应内容（JSON 格式）
        data = response.json()
        return data["geocodes"][0]["location"]
    else:
        raise RuntimeError("高德地图返回错误码: ", response.status_code)
