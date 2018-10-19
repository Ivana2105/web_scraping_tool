# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:32:42 2018

@author: Ivana-ETF
"""


import pandas as pd
from bs4 import BeautifulSoup

class HTMLTable_parse():
      
    def data_html_table(self, table):
    #number of table rows and logest row 
        n_row = 0   
        m = []        
        for row in table.find_all('tr'):
            td_tags = row.find_all('td')
            m.append(len(td_tags))
            n_row += 1
        mm = max(m)   
        
        #DataFrame for storing data
        df = pd.DataFrame(columns = range(0,mm),index= range(0,n_row)) 
        rows = 0
        for row in table.find_all('tr'):
            col = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[rows,col] = column.get_text().strip()
                col += 1
            if len(columns) > 0:
                rows += 1
                
        return df
    
    def tabs_html_table(self, table):
    #number of table rows and logest row 
        n_row = 0
        m = []
        for row in table.find_all('tr'):
            td_tags = row.find_all('td')
            m.append(len(td_tags))
            n_row += 1
        mm = max(m)
        
        #DataFrame for storing html elements
        df1 = pd.DataFrame(columns = range(0,mm),index= range(0,n_row)) 
        rows = 0
        for row in table.find_all('tr'):
            try: 
                pom = row['class']
            except:
                pom = ''
        
            col = 0
            columns = row.find_all('td')
            for column in columns:
                try:
                    pok = column['class']
                except:
                    pok = ''
                df1.iat[rows,col] = (pom,pok)
                col += 1
            if len(columns) > 0:
                rows += 1
        return df1