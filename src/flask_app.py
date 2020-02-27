# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:42:56 2020

@author: ramon
"""

from flask import render_template, request, redirect, url_for
from flask import Flask
from bokeh.embed import components
from bokeh.layouts import row, layout
from bokeh_map import *
from bokeh_system_state import *
from bokeh_historics import *
from bokeh_waterfall import *
from bokeh_user_act import *
import time
import threading
import os


app = Flask(__name__)
contActivos = 0
feature_names = ['15']
ips = {}


def elimina_ips():
    """
        Función creada a modo de determinar inactividad de usuario activo. Si pasan más de 5 minutos, elimina
        al usuario activo, pudiendo dar la posibilidad de acceso a otra persona, ya que solo permite un
        usuario activo.
    """
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
        except:
            pass

# Index page
@app.route('/')
def home():
    """
        Ruta principal de la página.
        Se fija si hay alguien activo, si no lo hay, setea usuario activo, le da un tiempo de inicio (para poder
        fijarse si está activo o inactivo) y lo redirige hacia el mapa. 
        En caso de haber un usuario activo, se le muestra a la persona una página que le avisa al usuario
        que ya hay alguien activo.
    """
    global contActivos, ips, wfActivo
    wfActivo = 0
    ip = request.remote_addr
    if contActivos == 0 or ip in ips.keys():
        ips[ip] = time.time()
        contActivos = 1
        return redirect(url_for('map_zones'))
    else:
        return redirect(url_for('user_act'))

@app.route("/logout")
def logout():
    """
        Esta función elimina al usuario activo de la lista cuando el mismo se desconecta voluntarimente
        y lo redirige a una página avisando al usuario que se desconectó.
    """
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
    """
        Esta función solamente muestra una página de muestra a un usuario que se quiere conectar cuando
        ya existe alguien activo.
    """
    global contActivos, wfActivo
    wfActivo = 0
    # Determine the selected feature
    div = usuario_activo()
    layout_b = layout(div)
    # Embed plot into HTML via Flask Render
    script, div = components(layout_b)
    return render_template("user_act.html")

@app.route('/wf')
def waterfall():
    """
        Muestra al usuario el waterfall, además de actualizar el contador de tiempo, ya que existe un usuario
        que está realizando cambios. En caso de no haber alguien, se le asigna un tiempo inicial.
    """
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
def system_state():
    """
        Muestra al usuario el estado del equipo, además de actualizar el contador de tiempo, ya que existe un usuario
        que está realizando cambios. En caso de no haber alguien, se le asigna un tiempo inicial.
    """
    global wfActivo, ips, contActivos
    wfActivo = 0
    contActivos = 1
    ip = request.remote_addr
    if ip in ips.keys():
        ips[ip] = time.time()
    else:
        ips[ip] = time.time()
    p, p2 = visualiza_estado()
    script, div = components(row(p, p2))
    return render_template("estado.html", script=script, div=div)

@app.route('/table')
def table_historics():
    """
        Muestra al usuario la tabla de históricos, además de actualizar el contador de tiempo, ya que existe un usuario
        que está realizando cambios. En caso de no haber alguien, se le asigna un tiempo inicial.
    """
    global wfActivo, ips, contActivos
    wfActivo = 0
    ip = request.remote_addr
    contActivos = 1
    if ip in ips.keys():
        ips[ip] = time.time()
    else:
        ips[ip] = time.time()
    data_table, range_slider, checkbox_eventos, div, checkbox_estado, div2, filtro_id, boton_sube, boton_baja, filtro_fecha_ini, filtro_fecha_fin, boton_filtra_fecha = visualiza_historicos()
    script, div = components(layout(row(layout(data_table, boton_sube, boton_baja), layout(range_slider, div, checkbox_eventos, div2, checkbox_estado, filtro_id, filtro_fecha_ini, filtro_fecha_fin, boton_filtra_fecha))))
    return render_template("historicos.html", script=script, div=div)


@app.route('/map')
def map_zones():
    """
        Muestra al usuario el mapa, además de actualizar el contador de tiempo, ya que existe un usuario
        que está realizando cambios. En caso de no haber alguien, se le asigna un tiempo inicial.
        
        Además, se está trabajando para que existan dos mapas de muestra, uno para usuarios autorizados y
        otro para los no autorizados, el autorizado permite realizar cambios, el otro no.
    """
    global contActivos, ips, wfActivo
    wfActivo = 0
    ip = request.remote_addr
    pathAutorizados = 'C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/usuariosAutorizados.txt'
    fileO = open(pathAutorizados, 'r')
    obj = fileO.read()
    fileO.close()
    usuariosHabilitados = obj.split('\n')
    if ip in usuariosHabilitados:
        usuarioAutorizado = 0
    else:
        usuarioAutorizado = 1
    if ip not in ips.keys() and contActivos == 0:
        ips[ip] = time.time()
        contActivos = 1
    # Determine the selected feature
    if usuarioAutorizado:
        current_feature_name = request.args.get("feature_name")
        if current_feature_name == None:
                current_feature_name = "15"
    
        # Create the plot
        p, checkbox_group, select, input_eventos, slider_intensidad, button, button2, div, div2, data_table, boton_muestra_eventos_zona, hover_t = create_map(current_feature_name)
        p.add_tools(hover_t)
        layout_b = layout(row(p, layout(div2, data_table)), row(select, layout(div,input_eventos, slider_intensidad), layout(button, boton_muestra_eventos_zona, button2), checkbox_group))
        # Embed plot into HTML via Flask Render
        script, div = components(layout_b)
        return render_template("iris_index3.html", script=script, div=div,
                feature_names=feature_names,  current_feature_name=current_feature_name)
    else:
        current_feature_name = request.args.get("feature_name")
        if current_feature_name == None:
                current_feature_name = "15"
    
        # Create the plot
        p, checkbox_group, select, input_eventos, slider_intensidad, button, button2, div, div2, data_table, boton_muestra_eventos_zona, hover_t = create_map(current_feature_name)
        p.tools = []
        p.add_tools(hover_t)
        checkbox_group.disabled = True
        select.disabled = True
        input_eventos.disabled = True
        slider_intensidad.disabled = True
        button.disabled = True
        button2.disabled = True
        boton_muestra_eventos_zona.disabled = True
        layout_b = layout(row(p, layout(div2, data_table)), row(select, layout(div,input_eventos, slider_intensidad), layout(button, boton_muestra_eventos_zona, button2), checkbox_group))
        # Embed plot into HTML via Flask Render
        script, div = components(layout_b)
        return render_template("iris_index4.html", script=script, div=div,
                feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
    

                                 
if __name__ == '__main__':
    """
        Inicia el thread correspondiente para eliminar ip's en caso de inactividad, además de iniciar la app
        de Flask.
    """
    thread_elimina_ips = threading.Thread(target=elimina_ips)
    thread_elimina_ips.setDaemon(True)
    thread_elimina_ips.start()
    app.secret_key = os.urandom(12)
    os.system("start cmd /k mueve_archivo_cambios.py")
    os.system("start cmd /k crea_archivo_db.py")
    app.run(port=5006, host='0.0.0.0')
