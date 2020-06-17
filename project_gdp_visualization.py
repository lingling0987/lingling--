#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：徐玲玲
日期：2020.6.12

"""

import csv
import math
import pygal
import pygal_maps_world.maps
wm = pygal_maps_world.maps.World() #导入需要使用的库


def read_csv_as_nested_dict(filename, keyfield, separator, quote): #读取原始csv文件的数据，格式为嵌套字典
    """
    输入参数:
      filename:csv文件名
      keyfield:键名
      separator:分隔符
      quote:引用符

    输出:
      读取csv文件数据，返回嵌套字典格式，其中外层字典的键对应参数keyfiled，内层字典对应每行在各列所对应的具体值
    """
    result={}
    with open(filename,newline="")as csvfile:
        csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csvreader:
            result[row[keyfield]]=row
    return result
   


pygal_countries = pygal.maps.world.COUNTRIES #读取pygal.maps.world中国家代码信息（为字典格式），其中键为pygal中各国代码，值为对应的具体国名(建议将其显示在屏幕上了解具体格式和数据内容）


def reconcile_countries_by_name(plot_countries, gdp_countries): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合
    """
    
    输入参数:
    plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
    gdp_countries:世行各国数据，嵌套字典格式，其中外部字典的键为世行国家代码，值为该国在世行文件中的行数据（字典格式)
    
    输出：
    返回元组格式，包括一个字典和一个集合。其中字典内容为在世行有GDP数据的绘图库国家信息（键为绘图库各国家代码，值为对应的具体国名),
    集合内容为在世行无GDP数据的绘图库国家代码
    """
    setA = set()
    dictA = {}
    for k,v in gdp_countries.items():
        crusial = set(v.values())
        if len(crusial) == 5:
            setA.add(from_value_to_key(k))
    for key,value in plot_countries.items():
        if value not in setA:
            dictA[key] = value
    tuple1 = (dictA,setA)
    return tuple1


def from_value_to_key(value):           
    for k,v in pygal_countries.items():
        if v == value:
            return k

def from_key_to_value(key):               
    for k,v in pygal_countries.items():
        if k == key:
            return v


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    输入参数:
    gdpinfo: 
	plot_countries: 绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
	year: 具体年份值
	
    输出：
    输出包含一个字典和二个集合的元组数据。其中字典数据为绘图库各国家代码及对应的在某具体年份GDP产值（键为绘图库中各国家代码，值为在具体年份（由year参数确定）所对应的世行GDP数据值。为
    后续显示方便，GDP结果需转换为以10为基数的对数格式，如GDP原始值为2500，则应为log2500，ps:利用math.log()完成)
    2个集合一个为在世行GDP数据中完全没有记录的绘图库国家代码，另一个集合为只是没有某特定年（由year参数确定）世行GDP数据的绘图库国家代码

   """
    dictB = {}
    setB = set()
    for key,value in gdpinfo.items():
        if from_value_to_key(key) in plot_countries[0]:               
            if value[year] != "":                                   
                aeee = float(value[year])
                dictB[from_value_to_key(key)] = math.log(aeee)
            else:                                                 
                setB.add(from_value_to_key(key))
    tuple2 = (dictB,setB,plot_countries[1])
    return tuple2     #返回元组
    


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      
      gdpinfo:gdp信息字典
      plot_countires:绘图库国家代码数据，字典格式，其中键为绘图库国家代码，值为对应的具体国名
      year:具体年份数据，以字符串格式程序，如"1970"
      map_file:输出的图片文件名
    
    目标：将指定某年的世界各国GDP数据在世界地图上显示，并将结果输出为具体的的图片文件
    提示：本函数可视化需要利用pygal.maps.world.World()方法
     

    """
    dictC = {}
    dictD = {}
    listD = list(gdpinfo[1])                             
    listE = list(gdpinfo[2])
    for values in listD:
        dictC[values] = "1"
    for a in listE:
        if a != None:                             
            dictD[a] = "1"
    
    wm.title = '全球GDP分布图'                      
    wm.add('%s'%year,gdpinfo[0])
    wm.add('missing from world bank',dictC)
    wm.add('no data at this year',dictD)
    wm.render_to_file(map_file)


    

    
pygal_countries = pygal.maps.world.COUNTRIES
print("欢迎使用世行GDP数据可视化查询")
print("----------------------")

year=input("请输入需查询的具体年份:")
l = read_csv_as_nested_dict("isp_gdp.csv","Country Name",",",'"')      
a = reconcile_countries_by_name(pygal_countries,l)                 
b = build_map_dict_by_name(l,a,year)                            
render_world_map(b,pygal_countries,year,"isp_gdp_world_name_%s.svg"%year)   
