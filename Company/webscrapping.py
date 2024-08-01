from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

def webscrapping():
    url = "https://www.nelomasi.com.np/2021/06/list-of-provinces-and-districts-in-nepal.html"
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    titles = soup.find_all("li")
    list = []
    for i in titles:
        i.find_all('b')
        result = i.text.strip()
        list.append(result)
    province_list = list[9:16]
    districts_list = list[16:93]
    dict = {
        province_list[0]:districts_list[0:14],
        province_list[1]:districts_list[14:22],
        province_list[2]:districts_list[22:35],
        province_list[3]:districts_list[35:46],
        province_list[4]:districts_list[46:58],
        province_list[5]:districts_list[58:68],
        province_list[6]:districts_list[68:78]
    }
    # 
    # with open('provincesanddistricts.csv','w') as data: 
    #   data.write(str(dict))
    
    with open('provincesanddistricts.csv','r') as data: 
      pass