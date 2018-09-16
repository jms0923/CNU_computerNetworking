#!/usr/bin/python3
import cgi, cgitb
import pygeoip
import subprocess
import re
# get data from input tag
form = cgi.FieldStorage()
print("Content-type:text/html")
print()
print('<html>')
print('<head>')
print('<meta charset="utf-8">')
print('<title>Traceroute</title>')
print('<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=a4da4568e24a16f1d82412bf7b4c653b"></script>')
print('<script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=APIKEY&libraries=services,clusterer,drawing"></script>')
print('</head>')
print('<body>')
print('<h2>Traceroute - Visualize on Kakao Map</h2>')
# get domain
print("<form method='get' action='hellohtml.cgi' >")
print("<input type='text' name='target'/>", "<input type='submit'/>")
print('</form>')

# argv_data is domain
argv_data = form.getvalue('target')

# open map
print('<div id="map" style="width:500px;height:400px;"></div>')
print('<script> var container = document.getElementById("map");')
print('var options = { ')
print('	center: new daum.maps.LatLng(36.366593, 127.344151),')
print('	level: 3 };')
print('var map = new daum.maps.Map(container, options);')
print('</script>')

# traceroute when enter domain
if(argv_data != None):
    TR = ['traceroute', str(argv_data)]  # make traceroute command
    #  universal_newlines=True      'out' convert byte to string
    proc = subprocess.Popen(TR, stdout=subprocess.PIPE, universal_newlines=True)
    out, err = proc.communicate()
    # get ip in () in 'out'
    p = re.compile('\([^()]*\)')
    IPList = p.findall(out)
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    # make list to save latitude and lognitude
    latitude = list()
    longitude = []
    IPLen = len(IPList)
    for i in range(0, len(IPList)):
        IPList[i] = IPList[i].replace('(', '')    # remove (, ) form IPList
        IPList[i] = IPList[i].replace(')', '')
        if i > 29:                                # # hop can't over 30
            break
        if gi.record_by_addr(IPList[i]) == None:  # if no geolocation information in databases
            latitude.append(None)
            longitude.append(None)

        else:                                     # have a geoloction info in databases
            latitude.append(gi.record_by_addr(IPList[i])['latitude'])
            longitude.append(gi.record_by_addr(IPList[i])['longitude'])

# make marker on map
print('<script>')
print('var positions = [')
for i in range(0, IPLen):              # convert data from python to javascript
    if latitude[i] != None:
        if i != IPLen-1:
            print('    {   title: "',i, '",')
            print('        latlng: new daum.maps.LatLng(',latitude[i], ', ',longitude[i],')  },')
        else:
            print('    {   title: "', i, '",')
            print('        latlng: new daum.maps.LatLng(',latitude[i], ', ',longitude[i],')  }')
print('];')

# image of point
print('var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";')
# draw maker in map
print('for (var i = 0; i < positions.length; i ++) {')
print('    var imageSize = new daum.maps.Size(24, 35);')
print('    var markerImage = new daum.maps.MarkerImage(imageSrc, imageSize);')
print('    var marker = new daum.maps.Marker({')
print('        map: map,')
print('        position: positions[i].latlng,')
print('        title : positions[i].title,')
print('    });')
print('}')
print('</script>')

# show IP, Latitude and Lognitude List
print('<H2>Destination : ', argv_data, '</H2>')
for i in range(0,IPLen):
    print('(', IPList[i], ') - (', latitude[i], ',', longitude[i], ')')
    print('<br>')

print('</body>')
print('</html>')