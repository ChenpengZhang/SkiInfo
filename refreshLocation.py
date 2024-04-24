from qgisUtils import *
import pandas as pd

'''
此文件是一个脚本文件，用来刷新班车站的地理位置数据
'''
df = pd.read_excel("data/shuttleBus.xlsx")
for index, row in df.iterrows():
    # 获取地理位置的经纬度信息字符串
    location_string = geoCode(row["出发地"], "北京")
    # 更新 DataFrame 中对应行的值
    df.at[index, "出发地经纬度"] = location_string
    print(index, row["出发地"], location_string)
# 将修改后的 DataFrame 保存回原始 Excel 文件，不保存索引列
df.to_excel("data/shuttleBus.xlsx", index=False)
