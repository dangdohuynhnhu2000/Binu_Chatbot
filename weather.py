from bs4 import BeautifulSoup
import requests
import json

f = open('data/province_code.json', encoding="utf-8")
prov_data = json.load(f)
f.close()

def Get_Url(prov_data, province):
    url = ""
    if province in prov_data.keys():
        url = "https://www.24h.com.vn/du-bao-thoi-tiet-c568.html?province=" + str(prov_data[province])
    return url

def Get_Temp_Status(url):
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
            temp = soup.find("span", {"class": "ndBig"}).text
    except:
        temp = ""   
    try:
        status = soup.find("span", {"class": "hTuong"}).text
    except:
        status = ""
    if not temp:
        try:
            temp = soup.find("span", {"class": "ndSmall"}).text
        except:
            temp = ""
        status = ""
    return temp, status

def Extract_Province(prov_data, question):
    question = question.replace('_', " ")
    for key in prov_data.keys():
        if key in question:
            return key
    return ""

def Get_Weather(prov_data, question):
    ask_user = False
    province = Extract_Province(prov_data, question)

    #nếu không tìm thấy địa điểm trong câu trả lời
    if not province:
        res = "Bạn vui lòng nói rõ tên tỉnh/thành phố cụ thể!"
        ask_user = True
        return ask_user, res

    url = Get_Url(prov_data, province)
    if not url:
        res = "Mình không biết đâu."
        return ask_user, res
    temp, status = Get_Temp_Status(url)
    if temp:
        if status:
            res = temp + ', ' + status
        else:
            res = 'Nhiệt độ: ' + temp
    else:
        res = "Mình không biết đâu."
    return ask_user, res

def Get_Temp(prov_data, question):
    ask_user = False
    province = Extract_Province(prov_data, question)
     #nếu không tìm thấy địa điểm trong câu trả lời
    if not province:
        res = "Bạn vui lòng nói rõ tên tỉnh/thành phố cụ thể!"
        ask_user = True
        return ask_user, res

    url = Get_Url(prov_data, province)
    if not url:
        res = "Mình không biết đâu."
        return ask_user, res
    temp, status = Get_Temp_Status(url)
    if temp:
        res = "Nhiệt độ: " + temp
    else:
        res = "Mình không biết đâu."
    return ask_user, res

