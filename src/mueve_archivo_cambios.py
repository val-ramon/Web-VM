#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:03:18 2020

@author: valramon
"""

import os
import shutil
import glob
import threading

archVistos = []
archNuevo = ''
hayArchNuevo = False

def miraArchivos(*args):
    global archVistos, archNuevo, hayArchNuevo
    while True:
        pathData = os.environ['USERPROFILE']+'/Downloads/'
        archivosCsv = glob.glob(pathData + 'change_emmited*.csv')
        archNuevo = ''
        for archivo in archivosCsv:
            if archivo not in archVistos:
                archNuevo = archivo
                archVistos.append(archivo)
                hayArchNuevo = True
                
        if hayArchNuevo:
            print (archNuevo)
        
    
miroArchNuevoThread = threading.Thread(target=miraArchivos)
miroArchNuevoThread.setDaemon(True)
miroArchNuevoThread.start()

pathData = os.environ['USERPROFILE']+'/Downloads/'
while True:
    if hayArchNuevo:
        source = pathData + archNuevo
        destination = os.environ['USERPROFILE']+'Downloads/bokeh_flask/bokeh_flask_vm/static/config/' + archNuevo
        shutil.copy(source, destination)
        os.remove(source)
