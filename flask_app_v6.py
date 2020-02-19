# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:42:56 2020

@author: ramon
"""

from flask import render_template, request, session, redirect, url_for, escape, flash, abort
from flask import Flask
from bokeh.embed import components
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource
from bokeh_figure_v5 import *
from flask_socketio import SocketIO
from sqlalchemy.orm import sessionmaker
from tabledef import *
import time
import threading
import os
import pandas as pd


app = Flask(__name__)
contActivos = 0
socketio = SocketIO(app)
cant_zonas = [5, 10, 20]
feature_names = [str(x) for x in cant_zonas]
ips = {}
dic_paginas = {'pagina': [0]}
df_paginas = pd.DataFrame(dic_paginas)
source_paginas = ColumnDataSource(df_paginas)


def elimina_ips():
    global ips, contActivos
    while True:
        horaActual = time.time()
        try:
            if len(ips) > 0:
                keys = ips.keys()
                for key in keys:
                    if horaActual - ips[key] > 300:
                        ips.pop(key)
                        print ('Usuario ' + key + ' inactivo durante mas de 5 minutos. Desconectado.')
                        contActivos = 0
                        break
#                        return render_template("logout.html")
        except:
            pass

@app.route('/')
def home():
    global contActivos, ips, source_paginas, wfActivo
    wfActivo = 0
    ip = request.remote_addr
    if contActivos == 0 or ip in ips.keys():
        session['logged_in'] = True
        ips[ip] = time.time()
        contActivos = 1
        if source_paginas.data['pagina'] == 0:
            return redirect(url_for('page'))
        else:
            return redirect(url_for('table'))
    else:
        return redirect(url_for('user_act'))

@app.route("/logout")
def logout():
    global contActivos, ips, wfActivo
    wfActivo = 0
    try:
        ips.pop(request.remote_addr)
        print ('Usuario ' + request.remote_addr + ' desconectado.')
        contActivos = 0
    except:
        pass
    return render_template("logout.html")

@app.route('/user_act')
def user_act():
    global contActivos, wfActivo
    wfActivo = 0
    # Determine the selected feature
    div = usuario_activo()
#    layout = column(p, row(select, column(div,text_input_eventos, text_input_intensidad), column(button, button2, boton_elimina_zona), checkbox_group), boton_agregar_zona, column(row(text_input_prog_ini, text_input_prog_fin), boton_confima_zona))  
    layout_b = layout(div)
    # Embed plot into HTML via Flask Render
    script, div = components(layout_b)
    return render_template("user_act.html")

@app.route('/wf')
def my_waterfall():
    global wfActivo, ips, contActivos
    contActivos = 1
    ip = request.remote_addr
    if ip in ips.keys():
        ips[ip] = time.time()
    else:
        ips[ip] = time.time()
    wfActivo = 1
    p = visualiza_waterfall()
    script, div = components(layout(p))
    return render_template("waterfall.html", script=script, div=div)

@app.route('/state')
def my_state():
    global wfActivo, ips, contActivos
    wfActivo = 0
    contActivos = 1
    ip = request.remote_addr
    if ip in ips.keys():
        ips[ip] = time.time()
    else:
        ips[ip] = time.time()
#    divTemp, divTens, divSnr, temp, tens, snr, divC, divV = visualiza_estado()
    p, p2 = visualiza_estado()
#    script, div = components(layout(row(layout(divTemp, divTens, divSnr), layout(temp, tens, snr), layout(divC, divV))))
    script, div = components(row(p, p2))
    return render_template("estado.html", script=script, div=div)

@app.route('/table')
def my_page_of_data_table():
    global wfActivo, ips, contActivos
    wfActivo = 0
    ip = request.remote_addr
    contActivos = 1
    if ip in ips.keys():
        ips[ip] = time.time()
    else:
        ips[ip] = time.time()
    data_table, boton_vuelve, range_slider, checkbox_eventos, div, checkbox_estado, div2, filtro_id, boton_sube, boton_baja = visualiza_historicos()
    script, div = components(layout(row(layout(data_table, boton_sube, boton_baja), layout(range_slider, div, checkbox_eventos, div2, checkbox_estado, filtro_id))))
    return render_template("historicos.html", script=script, div=div)
# Index page
@app.route('/map')
def page():
    global contActivos, ips, source_paginas, wfActivo
    wfActivo = 0
    ip = request.remote_addr
    if ip not in ips.keys() and contActivos == 0:
        ips[ip] = time.time()
        contActivos = 1
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
            current_feature_name = "15"

    # Create the plot
#    p, checkbox_group, select, text_input_eventos, text_input_intensidad, button, button2, div, boton_agregar_zona, text_input_prog_ini, text_input_prog_fin, boton_confima_zona, boton_elimina_zona = create_figure(current_feature_name)
    p, checkbox_group, select, input_eventos, slider_intensidad, button, button2, div, div2, data_table, boton_muestra_eventos_zona, buton_muestra_todos_eventos, source_cambia_paginas = create_figure(current_feature_name, source_paginas)
#    layout = column(p, row(select, column(div,text_input_eventos, text_input_intensidad), column(button, button2, boton_elimina_zona), checkbox_group), boton_agregar_zona, column(row(text_input_prog_ini, text_input_prog_fin), boton_confima_zona))  
#    layout_b = layout(p, row(select, layout(div,text_input_eventos, text_input_intensidad), layout(button, button2, boton_elimina_zona), checkbox_group), boton_agregar_zona, layout(row(text_input_prog_ini, text_input_prog_fin), boton_confima_zona))
#    buton_muestra_todos_eventos.on_click = my_page_of_data_table()
    layout_b = layout(row(p, layout(div2, data_table)), row(select, layout(div,input_eventos, slider_intensidad), layout(button, boton_muestra_eventos_zona, button2), checkbox_group))
    # Embed plot into HTML via Flask Render
    script, div = components(layout_b)
    return render_template("iris_index3.html", script=script, div=div,
            feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
    

                                 
if __name__ == '__main__':
    thread_elimina_ips = threading.Thread(target=elimina_ips)
    thread_elimina_ips.setDaemon(True)
    thread_elimina_ips.start()
    app.secret_key = os.urandom(12)
    socketio.run(app, port=5000, host='0.0.0.0')