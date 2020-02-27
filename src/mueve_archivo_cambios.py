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
import time

archVistos = []
archNuevo = ''
hayArchNuevo = False

def miraArchivos(*args):
    global archVistos, archNuevo, hayArchNuevo
    while True:
        try:
            pathData = os.environ['USERPROFILE']+'/Downloads/'
            os.chdir(pathData)
            archivosCsv = glob.glob('change_emmited*.csv')
            archNuevo = ''
            for archivo in archivosCsv:
                if archivo not in archVistos:
                    archNuevo = archivo
                    archVistos.append(archivo)
                    hayArchNuevo = True
                    
            if hayArchNuevo:
                source = archNuevo
                destination = os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/' + archNuevo
                shutil.copy(source, destination)
                os.remove(source)
                archVistos.remove(source)
                hayArchNuevo = False
        except:
            pass
        
    
miroArchNuevoThread = threading.Thread(target=miraArchivos)
miroArchNuevoThread.setDaemon(True)
miroArchNuevoThread.start()

pathData = os.environ['USERPROFILE']+'/Downloads/'

while True:
    if hayArchNuevo:
        time.sleep(1)
        print('Archivo movido de configuracion de zonas movido.')
