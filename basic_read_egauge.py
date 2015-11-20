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
print
print "Current timestamp is: " + (
    datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')
)
print
print "Current stats..."
# Get meter level results
for meter in tree.findall( 'meter' ):
    #print meter
    title = meter.attrib['title']
    if title == "Grid":
        power = meter.findtext("power")
        print "Grid usage: " + power + " watts"
    if title == "Solar":
        solar = meter.findtext("power")
    if title == "Solar2":
        solar2 = meter.findtext("power")
        print "Solar production: " + str((float(solar)+float(solar2))) + " watts"
    if title == "HVAC":
        hvac = meter.findtext("power")
        hvac = str(float(hvac)* -1)
        print "HVAC usage: " + hvac + " watts"
print
print "Cumulative stats..."
for meter in tree.findall( 'meter' ):
    #print meter
    title = meter.attrib['title']
    if title == "Grid":
        power = meter.findtext("energy")
        print "Grid has used: " + power + " kwh"
    if title == "Solar":
        solar = meter.findtext("energy")
    if title == "Solar2":
        solar2 = meter.findtext("energy")
        print "Solar has produced: " + str((float(solar)+float(solar2))) + " kwh"
    if title == "HVAC":
        hvac = meter.findtext("energy")
        hvac = str(float(hvac)* -1)
        print "HVAC has used: " + hvac + " kwh"


# Examine all the children of the tree
##for child in tree:
##    print child.tag, child.attrib
# Find all the elements
##for parts in tree:
##    print parts

