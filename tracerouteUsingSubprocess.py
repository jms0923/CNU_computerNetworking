import subprocess
import sys
import re
import pygeoip

# sys.argv[1]   get value in terminal
TR = ['traceroute', sys.argv[1]]  # make traceroute command
print('[Destination]   ', TR[1])

#  universal_newlines=True      'out' convert byte to string
proc = subprocess.Popen(TR, stdout=subprocess.PIPE, universal_newlines=True)
out, err = proc.communicate()

p = re.compile('\([^()]*\)')                    # get ip in () in 'out'
IPList = p.findall(out)
gi = pygeoip.GeoIP('GeoLiteCity.dat')

latitude = list()                               # make list to save latitude and lognitude
longitude = []

for i in range(0,len(IPList)):
    IPList[i] = IPList[i].replace('(', '')      # remove (, ) form IPList
    IPList[i] = IPList[i].replace(')', '')

    if gi.record_by_addr(IPList[i]) == None:    # if no geolocation information in databases
        print('[IP]   ', IPList[i], '   No Geolocation Information')
        latitude.append('No Geolocation Information')
        longitude.append('No Geolocation Information')

    else:                                       # have a geoloction info in databases
        latitude.append(gi.record_by_addr(IPList[i])['latitude'])
        longitude.append(gi.record_by_addr(IPList[i])['longitude'])
        print('[IP]   ', IPList[i], '   -   Lat : ', latitude[i], '   Lon : ', longitude[i])
