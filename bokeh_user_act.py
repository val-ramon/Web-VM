# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:38:44 2020

@author: valramon
"""

from bokeh.models.widgets import Div

def usuario_activo():
    div = Div(text="""Ya hay un usuario activo""", width=600, height=600)
    return div