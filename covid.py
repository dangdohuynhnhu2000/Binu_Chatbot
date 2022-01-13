from typing import List
from bs4 import BeautifulSoup
import requests
import json

def Get_Data():
    data = dict()
    
    url = "https://www.24h.com.vn/tong-hop-so-lieu-dich-covid-19-c972.html"
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find("table", {"class": "table"})
    
    #lấy dữ liệu covid cả nước
    thead = table.find("thead", {"class": "fixed-2"})
    ths = thead.findAll("th")
    #đưa vào dữ liệu: ca nhiễm hôm qua - ca tử vong hôm qua - tổng ca nhiễm - tổng ca tử vong
    data["cả nước"] = [ths[2].text, ths[5].text, ths[3].text, ths[4].text]
    
    #lấy dữ liệu covid từng tỉnh
    tbody = table.find("tbody")
    provs = tbody.findAll("tr")
    for prov in provs:
        tds = prov.findAll("td")
        #đưa vào dữ liệu: ca nhiễm hôm qua - ca tử vong hôm qua - tổng ca nhiễm - tổng ca tử vong
        prov_name = (tds[1].text).lower()
        data[prov_name] = [tds[2].text, tds[5].text, tds[3].text, tds[4].text]
    return data

def List_All_Province_Name(data):
    list_names = list(data.keys())
    list_names.extend(["tphcm", "hồ chí minh", "tp.hcm"])
    list_names.extend(["hn"])
    list_names.extend(["vũng tàu", "bà rịa vũng tàu", "bà rịa-vũng tàu", "bà rịa - vũng tàu"])
    list_names.extend(["huế", "thừa thiên - huế", "thừa thiên-huế"])
    list_names.extend( ["việt nam", "vn", "toàn quốc"])
    return list_names
        
def Map_Province_Name(prov_name):
    if prov_name in ["tphcm", "hồ chí minh", "tp.hcm"]:
        prov_name = "tp.hcm"
    elif prov_name == "hn":
        prov_name = "hà nội"
    elif prov_name in ["vũng tàu", "bà rịa vũng tàu", "bà rịa-vũng tàu", "bà rịa - vũng tàu"]:
        prov_name = "bà rịa - vũng tàu"
    elif prov_name in ["huế", "thừa thiên - huế", "thừa thiên-huế"]:
        prov_name = "thừa thiên huế"
    elif prov_name in ["việt nam", "vn", "toàn quốc"]:
        prov_name = "cả nước"
        
    if not prov_name:
        prov_name = "cả nước"
        
    return prov_name

def Extract_Province(data, question):
    question = question.replace('_', " ")
    list_names = List_All_Province_Name(data)
    for prov_name in list_names:
        if prov_name in question:
            return prov_name
    return ""

data = Get_Data()

def Get_Covid_Data(question, code):
    prov_name = Extract_Province(data, question)
    prov_name = Map_Province_Name(prov_name)
    
    #chuan hoa prov_name
    nor_prov_name = ""
    tokens = prov_name.split()
    for i in tokens:
        nor_prov_name += i.capitalize()
        nor_prov_name += " "
    
    res = "Tình hình covid " + nor_prov_name + ". "
    
    #lấy dữ liệu chung
    if code == 4:
        res += "Ca nhiễm mới hôm qua: " + data[prov_name][0] + '. '
        res += "Ca tử vong hôm qua: " + data[prov_name][1] + '. '
        res += "Tổng ca nhiễm: " + data[prov_name][2] + '. '
        res += "Tổng ca tử vong: " + data[prov_name][3] + '.'
    #lấy dữ liệu thành phần
    elif code == 0:
        res += "Ca nhiễm mới hôm qua: " + data[prov_name][0]
    elif code == 1:
        res += "Ca tử vong hôm qua: " + data[prov_name][1]
    elif code == 2:
        res += "Tổng ca nhiễm: " + data[prov_name][2]
    elif code == 3:
        res += "Tổng ca tử vong: " + data[prov_name][3]
    
    return res
         
    


