# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:42:57 2020

@author: edomene
"""

import pandas as pd
import bokeh
from bokeh.plotting import figure
import numpy as np
from collections import defaultdict
from bokeh.models import ColumnDataSource, HoverTool, ResetTool, SaveTool, DataTable, TableColumn, BoxZoomTool, OpenURL
from bokeh.models.widgets import CheckboxGroup, Button, Select, Slider, Div, TextInput, PreText, RangeSlider
from bokeh.models.ranges import Range1d
from bokeh.models import PolyDrawTool
from bokeh_callbacks_v5 import *
import os, glob, copy, pickle
from impar_bokeh import *
from osciloscopio_bokeh import *

def create_figure(n, source_cambia_paginas):
    #path donde se encuentre el csv con los datos de las zonas
    pathData = 'C:/Users/edomene/Downloads/'
    os.chdir(pathData)
    archivosCsv = glob.glob('change_emmited*.csv')
    dic_cuadrados = defaultdict(list)
    
    archivosDb = glob.glob('db*.db')
    dictHistoricos = defaultdict(list)
    fileO = open(archivosDb[-1], 'rb')
    while True:
        try:
            dataHist = pickle.load(fileO, encoding = 'bytes')
            dictHistoricos['id'].append(dataHist[1])
            dictHistoricos['vehi'].append(dataHist[10].encode("ascii"))
            dictHistoricos['progre'].append(round(dataHist[2], 2))
            dictHistoricos['fecha'].append(dataHist[5].strftime("%d/%m/%Y, %H:%M:%S"))
            dictHistoricos['estado'].append(dataHist[3])
        except:
            break
    for i in range(len(dictHistoricos['vehi'])):
        dictHistoricos['vehi'][i] = str(dictHistoricos['vehi'][i].decode())
        dictHistoricos['id'][i] = str(dictHistoricos['id'][i])
        dictHistoricos['progre'][i] = str(dictHistoricos['progre'][i])
        dictHistoricos['fecha'][i] = str(dictHistoricos['fecha'][i])
        dictHistoricos['estado'][i] = str(dictHistoricos['estado'][i])
    fileO.close()
    dataframe_historicos = pd.DataFrame(dictHistoricos)
#        del dataframe_historicos['index']
    source_historicos = ColumnDataSource(dataframe_historicos)
    source_historicos_muestra = ColumnDataSource(copy.deepcopy(dataframe_historicos))
    del source_historicos.data['index']
    del source_historicos_muestra.data['index']
    keys = dictHistoricos.keys()
    columns = [
        TableColumn(field='id', title='ID'),
        TableColumn(field='vehi', title='Vehiculo'),
        TableColumn(field='progre', title='Progresiva'),
        TableColumn(field='fecha', title='Fecha'),
        TableColumn(field='estado', title='Estado')
    ]
    
    data_table = DataTable(source=source_historicos_muestra, columns=columns, width=300, height=400)
    data_table.visible = False
    x, y = [], []
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
        dic_datos_lineas['RT_intensity'] = []
        largo_ducto = int(float(dic_datos_lineas['RT'][-1].split('pk')[-1]))
        n = len(dic_datos_lineas['RT'])
        lista_zonas = [(1.0,dic_datos_lineas['Intensity_tip'][k],dic_datos_lineas['Eventos_permitidos'][k]) for k in range(n)]
        for i in range(len(dic_datos_lineas['RT'])):
            dic_datos_lineas['RT_intensity'].append(np.arange(0, 50))
            dic_datos_lineas['RT'][i] = (float(dic_datos_lineas['RT'][i])) * np.ones(50)
            dic_datos_lineas['rel_int'][i] = float(dic_datos_lineas['rel_int'][i])
            x.append(dic_datos_lineas['RT'][i])
            y.append(dic_datos_lineas['RT_intensity'][i])
            if i != 0:
                dic_cuadrados['x'].append([[[dic_datos_lineas['RT'][i - 1][0], dic_datos_lineas['RT'][i - 1][0], dic_datos_lineas['RT'][i][0], dic_datos_lineas['RT'][i][0]]]])
            else:
                dic_cuadrados['x'].append([[[0, 0, dic_datos_lineas['RT'][i][0], dic_datos_lineas['RT'][i][0]]]])
            dic_cuadrados['y'].append([[[0, 50, 50, 0]]])
            if ("Ninguno" in dic_datos_lineas['Eventos_permitidos'][i]):
                dic_cuadrados['color'].append('White')
            else:
                dic_cuadrados['color'].append('Gray')
            dic_cuadrados['cont'].append(i)
                
    else:
        #si no existe un archivo, crea un diccionario con valores random para crear la figura del mapa
        largo_ducto = 30000
        dic_datos_lineas = defaultdict(list)
        int_fict=np.arange(50)
        order_loc=np.ones(50)
        
        
        
        n=int(n)
        choices=['Ninguno','Retroexcavadora/Camion']
        lista_zonas=[(1.0,'Zona '+str(k),np.random.choice(choices)) for k in range(n)]     
        #        zonas = []
        
        i = 0
        for scale, mz, evt_list in lista_zonas:
            dic_datos_lineas["RT"].append(order_loc*largo_ducto/n)
            dic_datos_lineas['ProgresivaIni'].append('pk'+str(round((order_loc[0] - 1)*int(largo_ducto/1000/n) + 338, 2)))
            dic_datos_lineas['ProgresivaFin'].append('pk'+str(round(order_loc[0]*int(largo_ducto/1000/n) + 338, 2)))
            dic_cuadrados['x'].append([[[(order_loc[0] - 1)*largo_ducto/n]]])
            dic_cuadrados['x'][i][0][0].append((order_loc[0] - 1)*largo_ducto/n)
            x.append(order_loc)
            order_loc=order_loc+1
            dic_cuadrados['x'][i][0][0].append((order_loc[0] - 1)*largo_ducto/n)
            dic_cuadrados['x'][i][0][0].append((order_loc[0] - 1)*largo_ducto/n)
            dic_datos_lineas["RT_intensity"].append(int_fict*scale)#norm(loc=120.4).pdf(RT_x) * 
            y.append(int_fict*scale)
            dic_cuadrados['y'].append([[[0, 50, 50, 0]]])
            dic_datos_lineas['Eventos_permitidos'].append(evt_list)
            dic_datos_lineas['Intensity_tip'].append(mz)
            dic_datos_lineas['rel_int'].append(round(np.random.normal(loc=0.9,scale=0.01),2))
            if ("Ninguno" in evt_list):
                dic_datos_lineas['color'].append('Gray')
                dic_cuadrados['color'].append('White')
            else:
                dic_cuadrados['color'].append('Gray')
            if (len(evt_list.split('/')) == 1 and "Ninguno" not in evt_list):
                dic_datos_lineas['color'].append('Orange')
            if (len(evt_list.split('/')) == 2 and "Ninguno" not in evt_list):
                dic_datos_lineas['color'].append('Orange')
            if (len(evt_list.split('/')) == 3 and "Ninguno" not in evt_list):
                dic_datos_lineas['color'].append('Orange')
            dic_cuadrados['cont'].append(i)
            i += 1
        dic_datos_lineas['RT'][-1].fill(largo_ducto)
    i = 0
    coor = {'x': x, 'y':y}
    data = pd.DataFrame(dic_datos_lineas)
    data2 = pd.DataFrame(coor)
    zona_elegida = ['Zona 0']
    data_modifica = {'zona': zona_elegida}
    #transforma diccionarios a dataframes
    data_a_modificar = pd.DataFrame(data_modifica)
    data_respaldo = pd.DataFrame(copy.deepcopy(dic_datos_lineas))
    data_cuadrados = pd.DataFrame(dic_cuadrados)
    #Create the data sources for plotting the data
    #luego transforma los dataframes en data sources para poder trabajarlos en bokeh
    source = ColumnDataSource(data)
    source2_respaldo = ColumnDataSource(data2)
    source3 = ColumnDataSource(data_a_modificar)
    source_respaldo = ColumnDataSource(data_respaldo)
    source_cuadrados = ColumnDataSource(data_cuadrados)
    
    
    x_limit_left=largo_ducto+0.1
    
    #aqui setea las herramientas a utilizar en el mapa
    tools = [ResetTool(), SaveTool(), BoxZoomTool()]
    
    #crea la figura del mapa
    p = figure(plot_width=1200, plot_height=600,x_range=(0,x_limit_left), y_range=Range1d(0,49), tools = tools)
    
    #le incrusta la imagen del mapa y crea las lineas de las zonas
    p.image_url(url=['static/mapa_vm3.jpg'], x=0, y=0, w=x_limit_left, h=49,anchor='bottom_left')
    ml=p.multi_line(xs='RT', ys='RT_intensity',  # estas 4 lineas dibujan las lines de las zonas
                 line_width=5, line_color='color', line_alpha=0.7,
                 hover_line_color='pink', hover_line_alpha=1.0,
                 source=source)
    
    #setea las etiquetas para ver en la herramienta que sirve para cuando se pasa el mouse sobre una linea de zona
    hover_t=HoverTool(show_arrow=False, tooltips=[
        ('Zona', '@Intensity_tip'),
        ('Inicio de zona', '@ProgresivaIni'),
        ('Fin de zona', '@ProgresivaFin'),
        ('Eventos permitidos', '@Eventos_permitidos'),
        ('Intensidad relativa', '@rel_int')
    ], renderers = [ml])
    
    p.add_tools(hover_t)
    
    #crea los sombreados de las zonas
    poli = p.multi_polygons(xs='x', ys = 'y', color = 'color', line_alpha = 0,fill_alpha = 0.3, source = source_cuadrados)
    poli.visible = True
    
    #agrega la posibilidad de manipular las lineas de las zonas
    draw_tool_l1 = PolyDrawTool(renderers=[ml])
    
    p.add_tools(draw_tool_l1)
#    p.toolbar.active_tap = draw_tool_l1
    
    p.xaxis.bounds=(0,n)
    p.yaxis.visible=False
    p.xaxis.visible=False
    
    
    oculta_zonas = ['Mostrar zonas']
    labels = [zona[1] for zona in lista_zonas]
    
    #crea los callbacks en javascript para cuando el script esta en ejecucion
    callback_checkbox = checkbox(source, source2_respaldo, source_respaldo, oculta_zonas, x, y)
    callback_guarda_zona = guarda_zona(source3)
    callback_evento = evento(source, source3, source_respaldo, source_cuadrados)
    callback_int = intensidad(source, source3, source_respaldo)
    
    eventos_perm = ["Ninguno", "Camioneta", "Camion", "Retroexcavadora"]
    
    #crea los distintos botones y herramientas a utilizar para el manejo del mapa, se crean en bokeh y funcionan con callbacks en javascript
    select = Select(title="Modificar zona:", value=source3.data['zona'][0], options=labels, callback = callback_guarda_zona)
    checkbox_group = CheckboxGroup(labels=oculta_zonas, active=[i for i in range (1)], callback=callback_checkbox)
    input_eventos = CheckboxGroup(labels=eventos_perm, active=[0], callback=callback_evento)
    slider_intensidad = Slider(start=0, end=1, value=0.5, step=.05, title="Intensidad relativa", callback = callback_int)
 
    callback_deshace_cambios = deshace_cambios(source, source_respaldo, source_cuadrados, input_eventos, slider_intensidad, eventos_perm, source3, draw_tool_l1)
    callback_download = download(source)
    text_input_prog_ini = TextInput(value='340', title='Progresiva de inicio')
    text_input_prog_fin = TextInput(value='342', title='Progresiva de fin')
    text_input_prog_fin.visible = False
    text_input_prog_ini.visible = False
    
    callback_confirma_zona = confirma_zona(source, source_respaldo, source_cuadrados, select, text_input_prog_ini, text_input_prog_fin)
    boton_confirma_zona = Button(label="Confirmar zona", button_type="success", callback = callback_confirma_zona)
    boton_confirma_zona.visible = False
    
    callback_agrega_zona = agrega_zona(text_input_prog_ini, text_input_prog_fin, boton_confirma_zona)
    
    callback_elimina_zona = elimina_zona(source, select)
    
    button = Button(label = "Rehacer mapa", button_type="success", callback = callback_deshace_cambios)
    
    button2 = Button(label="Aplicar cambios", button_type="warning", callback = callback_download)
    
    boton_agregar_zona = Button(label="Agregar zonas", button_type="warning", callback = callback_agrega_zona)
    
    boton_elimina_zona = Button(label="Eliminar zona", button_type="danger", callback = callback_elimina_zona)
    boton_elimina_zona.disabled = True
    
    div2 = Div(text="""<h2>Ultimos 10 eventos de zona:</h2>""", width=300, height=50)
    div2.visible = False
    
    callback_muestra_eventos_zona = muestra_eventos_zona(source, source_historicos, source_historicos_muestra, data_table, select, div2)
    callback_muestra_todos_eventos = muestra_todos_eventos(source_cambia_paginas)
    
    boton_muestra_eventos_zona = Button(label='Mostrar ultimos eventos de zona', button_type='success', callback=callback_muestra_eventos_zona)
    boton_muestra_eventos_zona.disabled = True
    
    buton_muestra_todos_eventos = Div(text="""<a href="/table" style = color: #fff>________Visualizar historicos_______</a>""", width=300, height=30, style={'font-size': '130%', 'color': '#fff', 'background-color': '#5cb85c', 'border-color': '#4cae4c', 'text-align': 'center'})
    callback_mouse = mouse_drag(source, source_cuadrados, source3, select, poli, slider_intensidad, input_eventos, eventos_perm, source_respaldo, largo_ducto)
    callback_mouse_end = mouse_end(poli, source_cuadrados, source, largo_ducto, draw_tool_l1, boton_elimina_zona, source_respaldo)
    callback_mouse_move = mouse_move(source, source_respaldo, source_cuadrados)
    callback_tap = tap(source, source_respaldo, source3, source_cuadrados, slider_intensidad, input_eventos, eventos_perm, select, poli, draw_tool_l1, boton_elimina_zona, boton_muestra_eventos_zona, data_table, div2)
    callback_mouse_guarda = mouse_guarda(source, source_respaldo, source_cuadrados)
    
    #detecta eventos realizados con mouse en la figura para llamar a callbacks que modificar la figura del mapa
    p.js_on_event(bokeh.events.Tap, callback_tap)
    p.js_on_event(bokeh.events.Pan, callback_mouse)
    p.js_on_event(bokeh.events.MouseMove, callback_mouse_move)
    p.js_on_event(bokeh.events.PanEnd, callback_mouse_end)
    div = Div(text="""Eventos Permitidos:""", width=200, height=10)
    
#    return p, checkbox_group, select, input_eventos, slider_intensidad, button, button2, div, boton_agregar_zona, text_input_prog_ini, text_input_prog_fin, boton_confirma_zona, boton_elimina_zona
    return p, checkbox_group, select, input_eventos, slider_intensidad, button, button2, div, div2, data_table, boton_muestra_eventos_zona, buton_muestra_todos_eventos, source_cambia_paginas

def usuario_activo():
    div = Div(text="""Ya hay un usuario activo""", width=600, height=600)
    return div

def visualiza_historicos():
    pathData = 'C:/Users/edomene/Downloads/'
    os.chdir(pathData)
    archivosCsv = glob.glob('db*.db')
    dictHistoricos = defaultdict(list)
    fileO = open(archivosCsv[-1], 'rb')
    while True:
        try:
            dataHist = pickle.load(fileO, encoding='bytes')
            dictHistoricos['id'].append(dataHist[1])
            dictHistoricos['vehi'].append(dataHist[10].encode("ascii"))
            dictHistoricos['progre'].append(round(dataHist[2], 2))
            dictHistoricos['fecha'].append(dataHist[5].strftime("%d/%m/%Y, %H:%M:%S"))
            dictHistoricos['estado'].append(dataHist[3])
        except:
            break
    for i in range(len(dictHistoricos['vehi'])):
        dictHistoricos['vehi'][i] = str(dictHistoricos['vehi'][i].decode())
        dictHistoricos['id'][i] = str(dictHistoricos['id'][i])
        dictHistoricos['progre'][i] = str(dictHistoricos['progre'][i])
        dictHistoricos['fecha'][i] = str(dictHistoricos['fecha'][i])
        dictHistoricos['estado'][i] = str(dictHistoricos['estado'][i])
    fileO.close()
    dictIteraCantHistoricos = {'cont': [0]}
    dataframeIteraCantHistoricos = pd.DataFrame(dictIteraCantHistoricos)
    dataframe_historicos = pd.DataFrame(dictHistoricos)
#        del dataframe_historicos['index']
    sourceIteraHistoricos = ColumnDataSource(dataframeIteraCantHistoricos)
    source_todos_historicos = ColumnDataSource(dataframe_historicos)
    source_historicos = ColumnDataSource(copy.deepcopy(dataframe_historicos[:500]))
    source_historicos_filtrado = ColumnDataSource(copy.deepcopy(dataframe_historicos[:500]))
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
        
    data_table = DataTable(source=source_historicos_filtrado, columns=columns, width=600, height=400, editable=False, reorderable=False)
    
    
    botonSube = Button(label = "Eventos siguientes", button_type="success")
    botonBaja = Button(label = "Eventos anteriores", button_type="success")
    botonBaja.disabled = True
    
    callback_boton_baja = boton_baja(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonSube)
    callback_boton_sube = boton_sube(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonBaja)
    
    botonSube.callback = callback_boton_sube
    botonBaja.callback = callback_boton_baja
    
    boton_vuelve = Div(text="""<a href="/" style = color: #fff>________Volver al mapa_______</a>""", width=300, height=30, style={'font-size': '130%', 'color': '#fff', 'background-color': '#5cb85c', 'border-color': '#4cae4c', 'text-align': 'center'})
    archivosCsv = glob.glob('change_emmited*.csv')
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
    dic_filtros = {}
    dic_filtros['rango_pk'] = [(338,368)]
    dic_filtros['rango_fecha']  = [0]
    dic_filtros['estado'] = [list(np.unique(source_historicos.data['estado']))]
    dic_filtros['vehiculo'] = [list(np.unique(source_historicos.data['vehi']))]
    dic_filtros['id'] = [1]
    dataframe_filtros = pd.DataFrame(dic_filtros)
    source_filtros = ColumnDataSource(dataframe_filtros)
    callback_filtra_rango_pk = filtra_rango_pk(source_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_vehiculos = filtra_vehiculos(source_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_estado = filtra_estado(source_historicos, source_historicos_filtrado, data_table, source_filtros)
    callback_filtra_id = filtra_id(source_historicos, source_historicos_filtrado, data_table, source_filtros)
    pkIni = float(dic_datos_lineas['ProgresivaIni'][0].split('pk')[1])
    pkFin = float(dic_datos_lineas['ProgresivaFin'][-1].split('pk')[1])
    range_slider = RangeSlider(start=pkIni, end=pkFin, value=(pkIni,pkFin), step=.1, title="Filtrar por progresivas", callback=callback_filtra_rango_pk)
    div = Div(text="""Filtrar por vehiculos:""", width=200, height=10)
    checkbox_eventos = CheckboxGroup(labels=list(np.unique(source_historicos.data['vehi'])), active=[x for x in range(len(list(np.unique(source_historicos.data['vehi']))))], callback = callback_filtra_vehiculos)
    div2 = Div(text="""Filtrar por estado:""", width=200, height=10)
    checkbox_estado = CheckboxGroup(labels=list(np.unique(source_historicos.data['estado'])), active=[x for x in range(len(list(np.unique(source_historicos.data['estado']))))], callback = callback_filtra_estado)
    filtro_id = TextInput(value='', title='Filtrar por id:', callback = callback_filtra_id)
    
    return data_table, boton_vuelve, range_slider, checkbox_eventos, div, checkbox_estado, div2, filtro_id, botonSube, botonBaja
    
def visualiza_estado():
#    divTemp = Div(text="""<h3>Temperatura del laser:</h3>""", width=200, height=50)
#    divTens = Div(text="""<h3>Tension del laser:</h3>""", width=200, height=50)
#    divC = Div(text="""<h3>°C</h3>""", width=200, height=50)
#    divV = Div(text="""<h3>V</h3>""", width=200, height=50)
#    divSnr = Div(text="""<h3>Relacion senial ruido:</h3>""", width=200, height=50)
#    temp = TextInput(value=str(round(np.random.uniform(low=23.0, high=25.0), 2)), title='', height=50, width=100)
#    tens = TextInput(value=str(round(np.random.uniform(low=2.4, high=2.6), 2)), title='', height=50, width=100)
#    snr = TextInput(value=str(round(np.random.uniform(low=275, high=325), 2)), height=50, width=100)
#    temp.disabled = True
#    tens.disabled = True
#    snr.disabled = True
#    fig.savefig('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/prueba.png')
    tools=[]
    p = figure(plot_width=600, plot_height=400,x_range=(0,1), y_range=Range1d(0,49), tools = tools)
    os.chdir('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/estado')
    imagenes_wf = glob.glob('impar*.png')
#    p.image_rgba(image=[fig], x=0, y=0, dw=10, dh=10)
    p.image_url(url=['static/estado/'+imagenes_wf[-1]], x=0, y=0, w=1, h=49,anchor='bottom_left')
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    p2 = figure(plot_width=600, plot_height=400,x_range=(0,1), y_range=Range1d(0,49), tools = tools)
    os.chdir('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/estado')
    imagenes_wf = glob.glob('osciloscopio*.png')
#    p.image_rgba(image=[fig], x=0, y=0, dw=10, dh=10)
    p2.image_url(url=['static/estado/'+imagenes_wf[-1]], x=0, y=0, w=1, h=49,anchor='bottom_left')
    p2.xaxis.visible = False
    p2.yaxis.visible = False
#    return divTemp, divTens, divSnr, temp, tens, snr, divC, divV
    return p, p2
    
def visualiza_waterfall():
    tools = []
    p = figure(plot_width=1200, plot_height=600,x_range=(0,1), y_range=Range1d(0,49), tools = tools)
    p.xaxis.visible = False
    p.yaxis.visible = False
    os.chdir('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/')
    imagenes_wf = glob.glob('wf_prueba*.jpg')
    indice_muestra = np.random.randint(low = 0, high = len(imagenes_wf) - 1)
    img_muestra = imagenes_wf[indice_muestra]
    
    #le incrusta la imagen del mapa y crea las lineas de las zonas
    p.image_url(url=['static/'+img_muestra], x=0, y=0, w=1, h=49,anchor='bottom_left')
    
    return p