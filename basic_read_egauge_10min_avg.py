#basic_read_egauge_10min_avg.py
#gfiske 2015


import urllib, datetime
from xml.etree import ElementTree as ET

# Enter eGauge name
eGauge = "egauge16231"

# Get XML from eGauge device
# url help from egauge tech support (egauge.net)
url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge-show?m&n=2&s=9&C"


# Parse the results
tree = ET.parse(urllib.urlopen(url)).getroot()

grid = ((int(tree[0][7][0].text)) * -1) / 600
solar = abs(int(tree[0][7][1].text)) / 600
hvac = int(tree[0][7][3].text) / 600
solar2 = abs(int(tree[0][7][4].text)) / 600

print "Averages for the last 10 minutes:"
print "grid: " + str(grid)
print "solar1: " + str(solar)
print "solar2: " + str(solar2)
print "total solar: " + str(solar + solar2)
print "hvac: " + str(hvac)

