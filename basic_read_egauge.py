#basic_read_eGauge.py
#reads energy data from eGauge
#gfiske Nov 2015

import urllib, datetime
from xml.etree import ElementTree as ET

# Enter eGauge name
eGauge = "egauge16231"

# Get XML from eGauge device
url = "http://" + eGauge + ".egaug.es/cgi-bin/egauge?noteam"

# Parse the results
tree = ET.parse(urllib.urlopen(url)).getroot()
timestamp  = tree.findtext("timestamp")
print "Current timestamp is: " + (
    datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')
)

# Get meter level results
for meter in tree.findall( 'meter' ):
    #print meter
    title = meter.attrib['title']
    if title == "Grid":
        power = meter.findtext("power")
        print "Grid usage is: " + power
    if title == "Solar":
        power = meter.findtext("power")
        print "Solar usage is: " + power

# Examine all the children of the tree
##for child in tree:
##    print child.tag, child.attrib
# Find all the elements
##for parts in tree:
##    print parts

