# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:32:42 2018

@author: Ivana-ETF
"""


import pandas as pd
import json
import re


# DataFrame for storing html elements
def tabs_html_table(table, elem, iid, clas):
    df1 = pd.DataFrame()
    attr = 'id' if iid else 'class'
    if elem == 'tr':
        rows = 0
        for row in table.find_all('tr'):
            try: 
                pom = row[attr]
            except:
                pom = ''
            else:
                if isinstance(pom, list):
                    pom = ','.join(pom)                
            col = 0
            columns = row.find_all('td')
            for column in columns:
                df1.loc[rows,col] = pom
                col += 1
            rows +=1
    elif elem =='td':
        print('This option has not yet been implemented')
        exit()

    return df1

#DataFrame for storing data
def data_html_table(table): 
    df = pd.DataFrame() 
    rows = 0
    for row in table.find_all('tr'):
        col = 0
        columns = row.find_all('td')
        for column in columns:
            df.loc[rows,col] = column.get_text().strip()
            col += 1
        rows += 1
            
    return df

def printing(df, start, end, sport):
    rows = df.shape[0]
    col = df.shape[1]
    for r in range(start,start + rows):
        x = { "sport": sport, "name": df.loc[r,0]}
        pp1 = 0
        pp2 = 0
        ll1 = 0
        ll2 = 0
        for c in range(col):
            pp = re.compile(r"[0-9]{3}-[0-9]{4}$")
            ll = re.compile(r"@")
            if pp.search(df.loc[r, c]):
                pp1 = r
                pp2 = c
            if ll.search(df.loc[r, c]):
                ll1 = r
                ll2 = c
        if pp1 and pp2:
            x["phone"] = df.loc[pp1,pp2]
        else:
            x["phone"] = ''
        if ll1 and ll2:
            x["mail"] = df.loc[ll1,ll2]
        else:
            x["mail"] = ''
        
            
        print(json.dumps(x))

def parse(table, sport, element, iid, index, clas):
    df = data_html_table(table)
    ind1 = []
    ind2 = []
    rows = 0
    if element in ['tr', 'td']:
        if index:
            print('There is no index in {}'.format(element))
            exit()
        if iid:
            val = iid
        else:
            val = clas
        df1 = tabs_html_table(table, element, iid, clas)
        for row in table.find_all('tr'):
            col = 0
            for column in row.find_all('td'):
                tab = df1.loc[rows, col]
                value = df.loc[rows, col]
                if (tab == val and (value == sport or value.upper() == sport or
                    value.lower() == sport)):
                    ind1.append(rows)
                    for r in range(rows+1, len(table.find_all('tr'))):
                        tabs = df1.loc[r, col]
                        if tabs == val:
                            ind2.append((r))
                    if not len(ind2):
                        ind2.append(len(table.find_all('tr')))
                col += 1        
            rows += 1
        if not len(ind1):
            print('There is no sport with name {} or atribut with value {}'\
                  .format(sport,  val))
        else:
            if ind1[0] == ind2[0] - 1:
                print('It is impossible to find information. Please improve your program.')
            else:
                start = ind1[0]+1
                end = ind2[0]-1
                printing(df.loc[start:end,:], start, end, sport)
    else:
        df1 = tabs_html_table(table, 'tr', False , True)
        for row in table.find_all('tr'):
            col = 0
            for column in row.find_all('td'):
                value = df.loc[rows, col]
                if (value == sport or value.upper() == sport or 
                    value.lower() == sport):
                    ind1.append(rows)
                    tab = df1.loc[rows, col]
                    for r in range(rows+1, len(table.find_all('tr'))):
                        tabs = df1.loc[r, col]
                        if tabs == tab:
                            ind2.append((r))
                    if not len(ind2):
                        ind2.append(len(table.find_all('tr')))
                col += 1        
            rows += 1
        if not len(ind1):
            print('There is no sport with name {}'.format(sport))
        else:
            if ind1[0] == ind2[0] - 1:
                print('It is impossible to find information. Please improve your program.')
            else:
                start = ind1[0]+1
                end = ind2[0]-1
                printing(df.loc[start:end,:], start, end, sport)
