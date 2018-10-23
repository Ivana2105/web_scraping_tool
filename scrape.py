# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 09:26:11 2018

@author: Ivana-ETF
"""

from bs4 import BeautifulSoup
import argparse
import requests
from HTMLTable import * 

   

def get_table(url, sport, element, iid, index, clas):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 \
               Safari/537.36'}
    res = requests.get(url,headers=headers)
    plain_text = res.text 
    soup = BeautifulSoup(plain_text,"html.parser")
    table = soup.find_all("table")
    
    # Check if there are tables on the page
    if len(table):
        # Check which html element is selected
        if element == "table":
            if index:
                if int(index) in range(len(table)):
                    parse(table[int(index)], sport, element, iid, index, clas)
                else:
                    print('There is no table with index {}'\
                          .format(str(index)))                   
            else:
                attr = 'id' if iid else 'class'
                val = iid if iid else clas
                b = 0
                for i in range(len(table)):
                    try:
                       pom = table[i][attr]
                    except:
                        print('There is no element {}'.format(val))
                        exit()
                    else:
                        if isinstance(pom, list):
                            pom=','.join(pom)
                        if pom == val:
                            b += 1
                            parse(table[i], sport, element, iid, index, clas)

                if not b:
                    print('There is no atribute {} with value {}'\
                          .format(attr, val))
                    
        else:
            parse(table[0], sport, element, iid, index, clas)
    else:
        b = 0
        for s in soup.find_all("div"):
            if s.find('iframe'):
               b += 1
               iframe_url = s.find('iframe')['src']
               get_table(iframe_url, sport, element, iid, index, clas)
        if not b:
            print('There is no table and iframe on the page')
            
            
def Main():
    """ 
    User select required input parameters - test url and sport as 
    required input parameters and optional parameters - html elements
    and html attributes 
     
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="choose the Staff Directory page URL to\
                        be scraped")
    parser.add_argument("sport", help="choose sport to be filtered")
    parser.add_argument("--html_elem", help="choose html element",\
                        choices=['table','tr','td'])
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--element_id')
    group.add_argument('--element_index')
    group.add_argument('--element_class')
    args = parser.parse_args()
    if (args.html_elem and args.element_id is None 
        and args.element_index is None and args.element_class is None):
        parser.error("--html_elem requires --element_id or --element_index \
                     or --element_class")
    
    url = args.url
    sport = args.sport
    element = args.html_elem
    iid = args.element_id
    index = args.element_index
    clas = args.element_class
                        
    get_table(url, sport, element, iid, index, clas)
    

if __name__=='__main__':
    Main()
