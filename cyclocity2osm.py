#!/usr/bin/env python
# -*- coding:utf-8 -*-

# @author: Alberto Molina Coballes
# @version: 0.1
# @licence: GPL-3

from lxml import etree
from urllib2 import urlopen

MINLAT="37.3074"
MAXLAT="37.4653"
MINLON="-6.0838"
MAXLON="-5.8249"

arbol = etree.parse("estaciones-sevici.xml")

nodos = arbol.xpath("/carto/markers/marker[not(contains(@name,'FUERA_DE_ESTACION'))]")

raiz = etree.Element("osm",attrib={"version":"0.6","upload":"true"})

arbol2 = etree.ElementTree(raiz)

bounds = etree.SubElement(raiz,"bounds",attrib={"minlat":MINLAT,
"maxlat":MAXLAT,"minlon":MINLON,"maxlon":MAXLON})

i=0
for nodo in nodos:
    i-=1
    estacion = etree.parse(urlopen("http://www.velib.paris.fr/service/stationdetails/seville/%s"
                                   % int(nodo.attrib["number"])))
    capacidad = estacion.xpath("/station/total/text()")[0]
    nuevo = etree.SubElement(raiz,"node",attrib={"id":"%s" % i,"action":"modify",
            "visible":"true","lat":nodo.attrib["lat"],"lon":nodo.attrib["lng"]})
    etree.SubElement(nuevo,"tag",attrib={"k":"amenity","v":"bicycle_rental"})
    etree.SubElement(nuevo,"tag",attrib={"k":"name","v":nodo.attrib["name"]})
    etree.SubElement(nuevo,"tag",attrib={"k":"network","v":"Sevici"})
    etree.SubElement(nuevo,"tag",attrib={"k":"operator","v":"JCDecaux"})
    etree.SubElement(nuevo,"tag",attrib={"k":"ref","v":nodo.attrib["number"]})
    etree.SubElement(nuevo,"tag",attrib={"k":"capacity","v":"%s" % capacidad})
    
salida = open("estaciones-sevici.osm","w")

salida.write(etree.tostring(arbol2,pretty_print=True,xml_declaration=True,encoding="utf-8"))