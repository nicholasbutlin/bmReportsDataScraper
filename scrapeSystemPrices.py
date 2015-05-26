# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:33:14 2014

@author: nickos
"""


import pandas as pd
from logging import logger
from datetime import date, timedelta

# =============================================================================


def dateRangeGen(start, end, delta):
    '''Generator for each date with start & end date & step in days'''
    curr = start
    while curr < end:
        yield curr
        curr += delta

# =============================================================================
# Variables
# =============================================================================
spotFile = '/home/nickos/spot.csv'
startDate = date(2014, 9, 27)
endDate = date(2015, 10, 16)

# Read the file if it exists
df = pd.read_csv(spotFile, index_col=False)


# For each date, get the spot data from BM Reports as a csv
for dateDay in dateRangeGen(startDate, endDate, timedelta(days=1)):
    logger.info(str(dateDay))
    url = """http://www.bmreports.com/bsp/additional/
             soapfunctions.php?output=CSV&dT=%s&
             element=SYSPRICE&submit=Invoke""" % str(date)

    dfa = pd.read_csv(url, skiprows=1, skipfooter=1,
                      names=['HH', 'SSP', 'SBP'], usecols=[2, 3, 4])

    dfa['date'] = dateDay
    df = pd.concat([df, dfa], axis=0)
    df.to_csv(spotFile, index=False)


df[df.HH <= 42][df.HH >= 14].SSP[df.SSP >= 0][df.SSP <= 100].hist(bins=50)
