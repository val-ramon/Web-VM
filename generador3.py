# -*- coding: utf-8 -*-
"""
Created on Mon May 21 15:30:59 2018

@author: Marco
"""

from matplotlib import cm
import time
import numpy as np
import webbrowser


def kml_cuerpo(file,coords,ind1,ind2,ind3,color_hex):
        
    file.write('	<StyleMap id="m_ylw-pushpin' + ind1 + '">\n')
    file.write('		<Pair>\n')
    file.write('			<key>normal</key>\n')
    file.write('			<styleUrl>#s_ylw-pushpin'+ ind2 +'</styleUrl>\n')
    file.write('		</Pair>\n')
    file.write('		<Pair>\n')
    file.write('			<key>highlight</key>\n')
    file.write('			<styleUrl>#s_ylw-pushpin_hl'+ ind3 +'</styleUrl>\n')
    file.write('		</Pair>\n')
    file.write('	</StyleMap>\n')
    file.write('	<Style id="s_ylw-pushpin'+ ind2 +'">\n')
    file.write('		<IconStyle>\n')
    file.write('			<scale>1.1</scale>\n')
    file.write('			<Icon>\n')
    file.write('				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n')
    file.write('			</Icon>\n')
    file.write('			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
    file.write('		</IconStyle>\n')
    file.write('		<LineStyle>\n')
    file.write('			<color>ff' + color_hex + '</color>\n')
    file.write('			<width>10</width>\n')
    file.write('		</LineStyle>\n')
    file.write('	</Style>\n')
    file.write('	<Style id="s_ylw-pushpin_hl'+ ind3 +'">\n')
    file.write('		<IconStyle>\n')
    file.write('			<scale>1.3</scale>\n')
    file.write('			<Icon>\n')
    file.write('				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>\n')
    file.write('			</Icon>\n')
    file.write('			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>\n')
    file.write('		</IconStyle>\n')
    file.write('		<LineStyle>\n')
    file.write('			<color>ff' + color_hex + '00</color>\n')
    file.write('			<width>10</width>\n')
    file.write('		</LineStyle>\n')
    file.write('	</Style>\n')
    file.write('	<Placemark>\n')
    file.write('		<name>ruta1</name>\n')
    file.write('		<styleUrl>#m_ylw-pushpin' + ind1 + '</styleUrl>\n')
    file.write('		<LineString>\n')
    file.write('			<tessellate>1</tessellate>\n')
    file.write('			<coordinates>\n')
    file.write('				' +  coords + ' \n')
    file.write('			</coordinates>\n')
    file.write('		</LineString>\n')
    file.write('	</Placemark>\n')       
    


cmap = cm.get_cmap('jet')
cant = 100.

color=cmap(0.1)
webbrowser.open('C:/Users/edomene/Downloads/earth/ruta1_p.kml')

for i in range(100):
    print (i)
    
    time.sleep(1)
    color=cmap(i/cant)


    file = open('ruta1_p.kml','w')  
    file.write('<?xml version="1.0" encoding="UTF-8"?> \n') 
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n')
    
    file.write('<Document>\n')
    file.write('	<name>ruta1.kml</name>\n') 
    
    file.write('	<NetworkLink>\n')
    file.write('		<Link>\n')
    file.write('			<href>C:/Users/edomene/Downloads/earth/ruta1_p.kml</href>\n')
    file.write('			<refreshMode>onInterval</refreshMode>\n')
    file.write('		    <refreshInterval>1</refreshInterval>\n')
    file.write('		</Link>\n')
    file.write('	</NetworkLink>\n')
    
    coords = '-61.29038652352855,-35.18684710207028,0 -61.25793268647514,-35.20281308431238,0 -61.23845602692159,-35.21521788619985,0'
    ind1 = str(1)
    ind2 = str(2)
    ind3 = str(3)
#    color_hex = '%02x%02x%02x' % (int(255*color[0]), int(255*color[1]), int(255*color[2]))
    color_hex = '%02x%02x%02x' % (int(np.random.randint(low=0, high=255)*color[0]), int(np.random.randint(low=0, high=255)*color[1]), int(np.random.randint(low=0, high=255)*color[2]))
    kml_cuerpo(file,coords,ind1,ind2,ind3,color_hex)

    coords = '-61.23845602692159,-35.21521788619985,0 -61.19082982643997,-35.23824203087184,0 -61.13668480398192,-35.26654594173061,0'
    ind1 = str(4)
    ind2 = str(5)
    ind3 = str(6)
    color_hex = '%02x%02x%02x' % (int(np.random.randint(low=0, high=200)*color[0]), int(np.random.randint(low=0, high=200)*color[1]), int(np.random.randint(low=0, high=200)*color[2]))
    kml_cuerpo(file,coords,ind1,ind2,ind3,color_hex)
    
    coords = '-61.19082982643997,-35.23824203087184,0 -61.13668480398192,-35.26654594173061,0 -61.09117680330844,-35.2948280674923,0'
    ind1 = str(7)
    ind2 = str(8)
    ind3 = str(9)
    color_hex = '%02x%02x%02x' % (int(np.random.randint(low=0, high=100)*color[0]), int(np.random.randint(low=0, high=100)*color[1]), int(np.random.randint(low=0, high=100)*color[2]))
    kml_cuerpo(file,coords,ind1,ind2,ind3,color_hex)
    
    coords = '-61.09117680330844,-35.2948280674923,0 -61.05431457567696,-35.31955539083103,0 -61.03696214395385,-35.33014522126225,0'
    ind1 = str(10)
    ind2 = str(11)
    ind3 = str(12)
    color_hex = '%02x%02x%02x' % (int(np.random.randint(low=0, high=20)*color[0]), int(np.random.randint(low=0, high=20)*color[1]), int(np.random.randint(low=0, high=20)*color[2]))
    kml_cuerpo(file,coords,ind1,ind2,ind3,color_hex)    
    
    
    file.write('</Document>\n')
    file.write('</kml>\n')
    file.close() 