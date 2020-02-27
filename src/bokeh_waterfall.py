# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:31:58 2020

@author: valramon
"""

from bokeh.plotting import figure
import numpy as np
from bokeh_callbacks import *
import os, glob, shutil, sys
from bokeh.models.ranges import Range1d

def visualiza_waterfall():
    """
        Esta función crea una figura de bokeh y va tomando las imágenes del waterfall para mostrarlas.
    """
    tools = []
    p = figure(plot_width=1200, plot_height=600,x_range=(0,1), y_range=Range1d(0,49), tools = tools)
    p.xaxis.visible = False
    p.yaxis.visible = False
    source = 'Y:/wf_web_vm/imagen_actual.jpg'
    try:
        destination = os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/wf/'+str(np.random.randint(0, high = sys.maxint))+'.png'
    except:
        destination = os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/wf/'+str(np.random.randint(0, high = 10000000))+'.png'
    imagenes_wf = glob.glob(os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/wf/*.png')
    try:
        for img in imagenes_wf:
            os.remove(img)
    except:
        pass
    shutil.copyfile(source, destination)
    os.chdir(os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/wf/')
    imagenes_wf = glob.glob('*.png')
    #le incrusta la imagen del mapa y crea las lineas de las zonas
    p.image_url(url=['static/wf/'+imagenes_wf[-1]], x=0, y=0, w=1, h=49,anchor='bottom_left')
    
    return p
