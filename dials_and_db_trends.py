#!/usr/bin/python
#dials_and_db_trends.py
#same as db_update_currentcost7.py
#updates database trend table in MySQL db and send data to google spreadsheet for live dials
#Greg Fiske 
# Original version Feb 2013
# Updated version with egauge Jan 2016

import serial,sys,MySQLdb
import xml.etree.ElementTree as ET # for XML parsing
import json
import urllib
import time
import gspread
import base64
import ConfigParser
import time
from oauth2client.client import SignedJwtAssertionCredentials

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
spreadsheet_name = 'Copy of home_dials new sheet'
###############################################################

#set up blank variables
totalwatts = 0
temp = 0
pv = 0
hvac = 0
enphasedata = 0

# Enter eGauge name
eGauge = "egauge16231"

# Get XML from eGauge device
url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge?noteam"


## Continuously call energy data from the egauge
while True:
    try:
        tree = ET.parse(urllib.urlopen(url)).getroot()
        
        # Get meter level data from tree
        for meter in tree.findall( 'meter' ):
            title = meter.attrib['title']
            if title == "Grid":
                net = meter.findtext("power")
            if title == "Solar":
                pv = meter.findtext("power")
            if title == "Solar2":
                enphasedata = meter.findtext("power")
                pvtotal =  str((float(pv)+float(enphasedata)))
            if title == "HVAC":
                hvac = meter.findtext("power")
                hvac = str(float(hvac)* -1)
                

        #update db
        db = MySQLdb.connect("127.0.0.1", db_user, db_passwd, "energy")
        myquery2 = "insert into trend values (DEFAULT, NOW()," + str(temp) + "," + str(net) + "," + str(pv) + "," + str(enphasedata) + "," + str(pvtotal) + "," + str(hvac) + ");"
        mycleanupquery = "delete from trend order by id limit 1;"
        cursor = db.cursor()
        cursor.execute(myquery2)
        cursor.execute(mycleanupquery)
        db.commit()
        db.close()

        #g = gspread.login(email, password)
        json_key = json.load(open('/home/pi/pi_energy/raspPi-e0a08639ebab.json'))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        g = gspread.authorize(credentials)
        worksheet = g.open('Copy of home_dials new sheet').get_worksheet(0)
        worksheet.update_cell(2,1,str(net))
        worksheet.update_cell(2,2,str(pvtotal))
        worksheet.update_cell(2,3,str(hvac))

        #set in a rest period
        time.sleep(10)
    except Exception,msg:
        filename = "/home/pi/db_error_log.txt"
        f = open(filename,"r+")
        f.readlines()
        now = time.localtime(time.time())
        curtime = time.asctime(now)
        f.write(curtime + "\n")
        f.write("The main function error is : " + str(msg) + "\n")
        f.write("\n")
        f.close()
        pass