# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:31:59 2020

@author: valramon
"""

from bokeh.plotting import figure
from bokeh_callbacks import *
import os, glob
from bokeh.models.ranges import Range1d


def visualiza_estado():
    """
        Esta función crea dos figuras de bokeh y va tomando las imágenes del estado del equipo para mostrarlas.
    """
    tools=[]
    p = figure(plot_width=600, plot_height=400,x_range=(0,1), y_range=Range1d(0,49), tools = tools)

    os.chdir(os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/estado/')
    imagenes_estado = glob.glob('impar*.png')
    
    p.image_url(url=['/static/estado/' + imagenes_estado[-1]], x=0, y=0, w=1, h=49,anchor='bottom_left')
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    p2 = figure(plot_width=600, plot_height=400,x_range=(0,1), y_range=Range1d(0,49), tools = tools)
    os.chdir(os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/estado/')
    imagenes_estado = glob.glob('osciloscopio*.png')

    p2.image_url(url=['/static/estado/' + imagenes_estado[-1]], x=0, y=0, w=1, h=49,anchor='bottom_left')
    p2.xaxis.visible = False
    p2.yaxis.visible = False

    return p, p2
    
