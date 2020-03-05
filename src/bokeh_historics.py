# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:31:57 2020

@author: valramon
"""

import pandas as pd
import numpy as np
from collections import defaultdict
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.models.widgets import CheckboxGroup, Button, Div, TextInput, RangeSlider
from bokeh_callbacks import *
import os, glob, copy, pickle, platform

def visualiza_historicos():
    """
        Esta función carga el archivo de la base de datos y la muestra al usuario en modo de table, permitiendo
        realizar distintos filtros sobre la misma.
    """
    
    pathData = os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/config/'
    archivosDb = glob.glob(pathData + '*.db')
    dictHistoricos = defaultdict(list)
    pyVersion = platform.python_version()
    if (int(pyVersion[0]) == 2):
        fileO = open(archivosDb[-1], 'r')
    else:
        fileO = open(archivosDb[-1], 'rb')
    while True:
        try:
            if (int(pyVersion[0]) == 2):
                dataHist = pickle.load(fileO)
            else:
                dataHist = pickle.load(fileO, encoding = 'bytes')
            dictHistoricos['id'].append(dataHist[1])
            dictHistoricos['vehi'].append(dataHist[10])
            dictHistoricos['progre'].append(round(dataHist[2], 2))
            dictHistoricos['fecha'].append(dataHist[5].strftime("%Y/%m/%d, %H:%M:%S"))
            dictHistoricos['estado'].append(dataHist[3])
        except:
            break
    for i in range(len(dictHistoricos['vehi'])):
        dictHistoricos['vehi'][i] = str(dictHistoricos['vehi'][i])
        dictHistoricos['id'][i] = str(dictHistoricos['id'][i])
        dictHistoricos['progre'][i] = str(dictHistoricos['progre'][i])
        dictHistoricos['fecha'][i] = str(dictHistoricos['fecha'][i])
        dictHistoricos['estado'][i] = str(dictHistoricos['estado'][i])
    fileO.close()
    dictIteraCantHistoricos = {'cont': [0]}
    dataframeIteraCantHistoricos = pd.DataFrame(dictIteraCantHistoricos)
    dataframe_historicos = pd.DataFrame(dictHistoricos)
    sourceIteraHistoricos = ColumnDataSource(dataframeIteraCantHistoricos)
    source_todos_historicos = ColumnDataSource(dataframe_historicos)
    source_historicos = ColumnDataSource(copy.deepcopy(dataframe_historicos[:500]))
    source_historicos_filtrado = ColumnDataSource(copy.deepcopy(dataframe_historicos[:0]))
    del source_historicos.data['index']
    del source_historicos_filtrado.data['index']
    keys = dictHistoricos.keys()
    columns = [
        TableColumn(field='id', title='ID'),
        TableColumn(field='vehi', title='Vehiculo'),
        TableColumn(field='progre', title='Progresiva'),
        TableColumn(field='fecha', title='Fecha'),
        TableColumn(field='estado', title='Estado')
    ]
        
    data_table = DataTable(source=source_todos_historicos, columns=columns, width=600, height=400, editable=True, reorderable=False)
    data_table.source = source_historicos_filtrado
    
    botonSube = Button(label = "Cargar eventos", button_type="success")
    botonBaja = Button(label = "Cargar menos eventos", button_type="success")
    botonBaja.visible = False
    
    callback_boton_baja = boton_baja(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonSube)
    callback_boton_sube = boton_sube(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonBaja)
    
    botonSube.callback = callback_boton_sube
    botonBaja.callback = callback_boton_baja
    
    archivosCsv = glob.glob('*.csv')
    mayor = 0
    #carga los datos de las zonas en un diccionario, lo carga como string, por eso la separacion por comas
    if len(archivosCsv) != 0:
        if len(archivosCsv) > 1:
            for archivo in archivosCsv:
                try:
                    if int(archivo.split(' ')[-1].split('.')[0][1:-1]) > mayor:
                        mayor = int(archivo.split(' ')[-1].split('.')[0][1:-1])
                        archNuevo = archivo
                except:
                    pass
        else:
            archNuevo = archivosCsv[0]
        archCsv = open(archNuevo, 'r')
        data = archCsv.read()
        archCsv.close()
        keys = data.split('\n')[0].split(',')
        data = data.split('\n')[1:]
        dictData = defaultdict(list)
        j = 0
        for i in range(len(data)):
            for key in keys:
                dictData[key].append(data[i].split(',')[j])
                j += 1
            j = 0
        dic_datos_lineas = dictData
    pkIni = float(dic_datos_lineas['ProgresivaIni'][0].split('pk')[1])
    pkFin = float(dic_datos_lineas['ProgresivaFin'][-1].split('pk')[1])
    dic_filtros = {}
    dic_filtros['rango_pk'] = [(pkIni,pkFin)]
    dic_filtros['rango_fecha']  = [[dictHistoricos['fecha'][0].split(',')[0] ,dictHistoricos['fecha'][-1].split(',')[0] ]]
    dic_filtros['estado'] = [list(np.unique(source_todos_historicos.data['estado']))]
    dic_filtros['vehiculo'] = [list(np.unique(source_todos_historicos.data['vehi']))]
    dic_filtros['id'] = [1]
    dataframe_filtros = pd.DataFrame(dic_filtros)
    source_filtros = ColumnDataSource(dataframe_filtros)
    callback_filtra_rango_pk = filtra_rango_pk(source_todos_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_vehiculos = filtra_vehiculos(source_todos_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_estado = filtra_estado(source_todos_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_id = filtra_id(source_todos_historicos, source_historicos_filtrado, data_table, source_filtros)
    
    callback_filtra_fecha_ini = filtra_fecha_ini(source_filtros)
    callback_filtra_fecha_fin = filtra_fecha_fin(source_filtros)
    callback_filtra_fecha = filtra_fecha(source_todos_historicos, source_historicos_filtrado, data_table, source_filtros)
    
    range_slider = RangeSlider(start=pkIni, end=pkFin, value=(pkIni,pkFin), step=.1, title="Filtrar por progresivas", callback=callback_filtra_rango_pk)
    div = Div(text="""<b>Filtrar por vehiculos:</b>""", width=200, height=10)
    checkbox_eventos = CheckboxGroup(labels=list(np.unique(source_todos_historicos.data['vehi'])), active=[x for x in range(len(list(np.unique(source_historicos.data['vehi']))))], callback = callback_filtra_vehiculos)
    div2 = Div(text="""<b>Filtrar por estado:</b>""", width=200, height=10)
    checkbox_estado = CheckboxGroup(labels=list(np.unique(source_todos_historicos.data['estado'])), active=[x for x in range(len(list(np.unique(source_historicos.data['estado']))))], callback = callback_filtra_estado)
    div_id = Div(text = '<b>Filtrar por id:</b>', width=200, height=10)
    filtro_id = TextInput(value='', callback = callback_filtra_id)

    div_fecha_i = Div(text = '<b>Fecha inicial a filtrar:</b>', width=200, height=10)
    filtro_fecha_ini = TextInput(value='AAAA/MM/DD', width=200, callback=callback_filtra_fecha_ini)
    div_fecha_f = Div(text = '<b>Fecha final a filtrar:</b>', width=200, height=10)
    filtro_fecha_fin = TextInput(value='AAAA/MM/DD', width=200, callback=callback_filtra_fecha_fin)

    div_filtro_fecha = Div(text="""<b class = 'adver'>Advertencia:</b> El formato de fechas debe ser <b>AAAA/MM/DD</b> para un filtrado correcto""", width=200, height=60, css_classes = ['div_adver'])

    boton_filtra_fecha = Button(label = "Filtrar fechas", button_type="success", callback=callback_filtra_fecha)

    return data_table, range_slider, checkbox_eventos, div, checkbox_estado, div2, filtro_id, div_id, botonSube, botonBaja, filtro_fecha_ini, div_fecha_i, filtro_fecha_fin, div_fecha_f, div_filtro_fecha, boton_filtra_fecha
