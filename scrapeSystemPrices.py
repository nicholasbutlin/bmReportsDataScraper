# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:33:14 2014

@author: nickos
"""


import pandas as pd
from datetime import date, timedelta
import logging
import os

# =============================================================================
# Basic Configurations, files and logging
# =============================================================================

# set the base directory as the current one
baseDir = os.path.dirname(os.path.realpath(__file__))

# Remove any existing logging handlers
logging.getLogger('').handlers = []

# Configure logging to file
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=baseDir+'/sysPrice.log',
                    level=logging.DEBUG)

# Log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

# =============================================================================


def dateRangeGen(start, end, delta):
    '''Generator for each date in range with start & end date & step in days'''
    curr = start
    while curr < end:
        yield curr
        curr += delta

# =============================================================================
# Variables
# =============================================================================
spotFile = baseDir+'/spot.csv'
startDate = date(2015, 01, 01)
endDate = date(2015, 05, 24)

# =============================================================================
# Start the script
# =============================================================================
logging.info('Starting Scrape from %s to %s', str(startDate), str(endDate))

# Read the spot file if it exists
try:
    df = pd.read_csv(spotFile, index_col=False)
except:
    df = pd.DataFrame()
    logging.warning('No current spot file')

# For each date, get the spot data from BM Reports as a csv
for dateDay in dateRangeGen(startDate, endDate, timedelta(days=1)):
    logging.debug(str(dateDay))

    url = ('http://www.bmreports.com/bsp/additional/soapfunctions.php?'
           'output=CSV&dT=%s&element=SYSPRICE&submit=Invoke') % str(dateDay)

    dfa = pd.read_csv(url, skiprows=1, skipfooter=1,
                      names=['HH', 'SSP', 'SBP'],
                      usecols=[2, 3, 4],
                      engine='python')

    dfa['date'] = dateDay
    df = pd.concat([df, dfa], axis=0)
    df.to_csv(spotFile, index=False)

logging.info('Finished scrape')
