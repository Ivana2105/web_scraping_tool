# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:29:30 2018

@author: Ivana-ETF
"""

from bs4 import BeautifulSoup
import argparse
import requests
from HTMLTable import * 
import sys

   

def get_table(url, sport, element, iid, index, clas):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
               ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
               ' Safari/537.36'}
    res = requests.get(url, headers=headers)
    plain_text = res.text 
    soup = BeautifulSoup(plain_text, 'html.parser')
    table = soup.find_all('table')
    
    # Check if there are tables on the page
    if len(table):
        # Check which html element is selected
        if element == "table":
            if iid or clas :
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
                    print('There is no attribute {} with value {}'
                          .format(attr, val))                 
            else:
                if int(index) in range(len(table)):
                    parse(table[int(index)], sport, element, iid, index, clas)
                else:
                    print('There is no table with index {}'
                          .format(str(index)))  
                    
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
            
def parse_args(args):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="choose the Staff Directory page URL to "
                        "be scraped")
    parser.add_argument("sport", help="choose sport to be filtered")
    parser.add_argument("--html_elem", help="choose html element",\
                        choices=['table','tr','td'])
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--element_id')
    group.add_argument('--element_index')
    group.add_argument('--element_class')
    
    return parser.parse_args(args)            
            
def Main():

    parser = parse_args(sys.argv[1:])
    if (parser.html_elem and parser.element_id is None 
        and parser.element_index is None and parser.element_class is None):
        print('--html_elem requires --element_id or --element_index ' 
              'or --element_class')
        exit()
                            
    get_table(parser.url, parser.sport, parser.html_elem, parser.element_id, 
              parser.element_index, parser.element_class)
    

if __name__=='__main__':
    Main()
    
    


