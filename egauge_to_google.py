#!/usr/bin/env python
###############################################################################
# egauge_to_google.py 2009-8-17
#
# Project:  egauge
# Purpose:  The purpose of this script is to collect egauge data from device and
#           post it to a Google Spreadsheet
# Author:   Greg Fiske, gfiske@whrc.org
#
###############################################################################

import xml.etree.ElementTree as ET # for XML parsing
import urllib, datetime
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
url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge?noteam"

#########################################
#          PULL FROM EGAUGE       #
#########################################

def pullFromDevice():
    # Read XML from eGauge device.  Try again if nothing is returned.
        # Parse the results
    tree = ET.parse(urllib.urlopen(url)).getroot()
    timestamp  = tree.findtext("timestamp")
    # Get meter level results
    for meter in tree.findall( 'meter' ):
        #print meter
        title = meter.attrib['title']
        if title == "Grid":
            grid = meter.findtext("power")
        if title == "Solar":
            solar = meter.findtext("power")
        if title == "HVAC":
            hvac = meter.findtext("power")
            hvac = str(float(hvac)* -1)
    return timestamp,grid,solar,hvac

data = pullFromDevice()


cur_time = (
        datetime.datetime.fromtimestamp(
            int(data[0])
        ).strftime('%Y-%m-%d %H:%M:%S')
    )
cur_grid = data[1]
cur_solar = data[2]
cur_hvac = data[3]

#print cur_time
#print cur_grid
#print cur_solar
#print cur_hvac

try:
    #enter the data into the google spreadsheet
    rowToAdd = (cur_time,cur_grid,cur_solar,cur_hvac)
    json_key = json.load(open('/home/pi/pi_energy/raspPi-e0a08639ebab.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
    g = gspread.authorize(credentials)
    worksheet = g.open('home_egauge16231').get_worksheet(0)
    worksheet.append_row(rowToAdd)
    print "...row add success"
except:
    print "...row add fail"
