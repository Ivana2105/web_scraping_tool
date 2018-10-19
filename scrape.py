# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 09:26:11 2018

@author: Ivana-ETF
"""

import argparse
import requests
from bs4 import BeautifulSoup
from HTMLTable import HTMLTable_parse
import json


def parse1(d,num,sport):
    '''    
    on the basis of a DataFrame with html tags, function finds cells that are of interest,
    takes the cell indexes and finds data in the DataFrame with the data
    
    '''
    ind=[]
    for i in range(d[0].shape[0]):
        for j in range(d[0].shape[1]):
            if d[1].loc[i,j] == (['sport-name'], ['hidden-phone']):
                ind.append([i,j])
    
    for i in range(len(ind)):
        if d[0].loc[ind[i][0],ind[i][1]] == sport:
            if i == len(ind)-1:
                st = ind[i][0]
                end = d[0].shape[0]
            else:
                st = ind[i][0]
                end = ind[i+1][0]
            for i in range(st+2,end):
                x = {
                        "sport": sport,
                        "name": d[0].loc[i,0],
                        "position": d[0].loc[i,2],
                        "phone": d[0].loc[i,3],
                        "email": d[0].loc[i,4]
                        }
                print(json.dumps(x))

def parse2(d,num,sport):
    pass

def parse3(d,num,sport):
    pass           


def get_table(url):
    
    #reading the source code for a web page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res=requests.get(url,headers=headers)
    plain_text=res.text 
    soup=BeautifulSoup(plain_text,"html.parser")
    tabl = soup.find_all("table")

    if len(tabl)==0:#table doesn't exist; if iframe exist 
#        if soup.find("div",{'class': 'article-content'}).find('iframe'):            
#            get_table(soup.find("div",{'class': 'article-content'}).find('iframe')['src'])
        pass
    elif len(tabl)==1:
        hp = HTMLTable_parse()
        data = hp.data_html_table(tabl[0]) 
        tags = hp.tabs_html_table(tabl[0])
        return(data, tags)
    else:
        hp = HTMLTable_parse()
        data = hp.data_html_table(tabl[1])
        tags = hp.tabs_html_table(tabl[1])
        return(data, tags)

    

def Main():
    
# user select test url and sport    
    parser = argparse.ArgumentParser()
    parser.add_argument("url", choices=['http://www.goseattleu.com/StaffDirectory.dbml', 'https://athletics.arizona.edu/StaffDirectory/index.asp', 'http://www.astateredwolves.com/ViewArticle.dbml?ATCLID=207138','https://arizonawildcats.com/sports/2007/8/1/207969432.aspx'], help="choose the Staff Directory page URL to be scraped")
    parser.add_argument("sport", help="choose sport to be filtered")
#    parser.add_argument("--html_element", help="choose html element")
    args = parser.parse_args()
    if args.url == 'http://www.goseattleu.com/StaffDirectory.dbml':
        num = 1
        url = 'http://www.goseattleu.com/StaffDirectory.dbml'
    if args.url == 'https://athletics.arizona.edu/StaffDirectory/index.asp':
        num = 2
        url = 'https://athletics.arizona.edu/StaffDirectory/index.asp'
    if args.url =='http://www.astateredwolves.com/ViewArticle.dbml?ATCLID=207138':
        num = 3
        url = 'http://www.astateredwolves.com/ViewArticle.dbml?ATCLID=207138'
    if args.url == 'https://arizonawildcats.com/sports/2007/8/1/207969432.aspx':
        num = 4
        url = 'https://arizonawildcats.com/sports/2007/8/1/207969432.aspx'
# for a specific url, function returns 2 DataFrames with data and html elements from the table 
    d = get_table(url)
# function returns desired information in JSON format
    if num==1:
        parse1(d, num, args.sport)
    elif num==2:
        parse2(d, num, args.sport)
    elif num==3:
        parse3(d, num, args.sport)
    else:
        pass


if __name__=='__main__':
    Main()