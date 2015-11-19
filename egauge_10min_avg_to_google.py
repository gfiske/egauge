#!/usr/bin/env python
###############################################################################
# egauge_10min_avg_to_google.py 2015-11-17
#
# Project:  egauge
# Purpose:  The purpose of this script is to average energy data every 10 minutes
#           and send it to a Google Spreadsheet
#
# Author:   Greg Fiske, gfiske@whrc.org
#
###############################################################################

import xml.etree.ElementTree as ET # for XML parsing
import urllib, time
import json
import gspread
import base64
import ConfigParser
from oauth2client.client import SignedJwtAssertionCredentials
import os,sys,time
import string
###############################################################
config = ConfigParser.RawConfigParser()
config.read('/home/pi/gfiske.cfg')
db_user = config.get('section1', 'db_user')
db_passwd = config.get('section1', 'db_passwd')
g_user = config.get('section1', 'g_user')
g_passwd = config.get('section1', 'g_passwd')
db_user = db_user.decode('base64','strict')
db_passwd = db_passwd.decode('base64','strict')
email = g_user.decode('base64','strict')
password = g_passwd.decode('base64','strict')[0:15]
spreadsheet_name = 'home_egauge16231'
###############################################################

# Enter eGauge name
eGauge = "egauge16231"
# Get XML from eGauge device
url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge-show?m&n=2&s=9&C"

#########################################
#          PULL FROM EGAUGE       #
#########################################
def pullFromDevice():
    # Parse the results
    tree = ET.parse(urllib.urlopen(url)).getroot()
    grid = ((int(tree[0][7][0].text)) * -1) / 600
    solar = abs(int(tree[0][7][1].text)) / 600
    if solar <= 10:
        solar = 0
    hvac = int(tree[0][7][3].text) / 600
    solar2 = abs(int(tree[0][7][4].text)) / 600
    if solar2 <= 10:
        solar2 = 0
    totalsolar = solar + solar2
    return grid,solar,solar2,totalsolar,hvac

try:
    data = pullFromDevice()
except:
    print "device pull failed"

#########################################
#          EDIT SHEET            #
#########################################

try:
    rowToAdd = (time.strftime('%m/%d/%Y'),time.strftime('%H:%M:%S'),str(data[0]),str(data[1]),str(data[2]),str(data[3]), str(data[4])) #date, time, grid, solar1, solar2, total solar, hvac
    json_key = json.load(open('/home/pi/pi_energy/raspPi-e0a08639ebab.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    g = gspread.authorize(credentials)
    worksheet = g.open('home_egauge16231').get_worksheet(0)
    worksheet.append_row(rowToAdd)
    print "...row add success"
except:
    print "...row add fail"
