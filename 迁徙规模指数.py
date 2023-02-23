# -*- coding: utf-8 -*-
"""
@Time: 2023/2/23 8:10
@Author: Songyx
@File: 迁徙规模指数.py
@IDE: PyCharm
"""
import requests  # 导入请求模块
import json  # 导入json模块
import time  # 导入时间模块
import xlsxwriter
from City_code import CitiesCode, ProvinceCode


def migration_index(FileTittle, classname, direction, CodeDict):  # CodeDict字典里所有城市的迁徙规模指数，以全国列表形式列出
    if direction == 'in':
        nameofdire = '迁入'
    if direction == 'out':
        nameofdire = '迁出'
    #######创建一个workbook########
    workbook = xlsxwriter.Workbook(f'{FileTittle} {nameofdire}规模指数.xlsx')
    worksheet = workbook.add_worksheet('Sheet')
    #################写入行头各城市代码及其城市名###############
    if direction == 'in':
        nameofdire = '迁入'
    if direction == 'out':
        nameofdire = '迁出'
    CitiesOrder = {}  # 存放城市序号的空字典
    worksheet.write(0, 0, '城市代码')  # 写入行头
    worksheet.write(0, 1, '城市')  # 写入行头
    times = 1
    for key, value in CodeDict.items():
        worksheet.write(times, 0, str(value))  # 写入城市代码
        worksheet.write(times, 1, str(key))  # 写入城市名
        CitiesOrder[str(key)] = times  # 写入城市序号字典
        times += 1
    ########################开始抓取数据##############################
    for Area, Code in CodeDict.items():
        url = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={classname}&id={Code}&type=move_{direction}'
        print(f'{Area}:{url}')
        response = requests.get(url, timeout=2)  # #发出请求并json化处理
        time.sleep(3)
        r = response.text[4:-1]  # 去头去尾
        data_dict = json.loads(r)  # 字典化
        if data_dict['errmsg'] == 'SUCCESS':
            data_list = data_dict['data']['list']
            counter_date = 2  # 日期计数器
            datelist = []
            for date, index in data_list.items():  # 按日期排序
                datelist.append(date)
            datelist.sort()
            for date in datelist:
                index = data_list[date]
                # print(f'{date} : {index}')
                worksheet.write(0, counter_date, float(date))
                worksheet.write(CitiesOrder[str(Area)], counter_date, float(index))
                counter_date += 1  # 日期计数器自加一
        else:
            print('错误')
    workbook.close()


quanguo = {'全国': 0}  # 全国编码

if __name__ == "__main__":
    migration_index('全国', 'country', 'out', ProvinceCode)
    migration_index('全国', 'conuntry', 'in', ProvinceCode)

    print('全部完成')
