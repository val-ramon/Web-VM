# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:42:57 2020

@author: valramon
"""

from bokeh.models import  CustomJS
import os
#Callbacks writed in JS for the logic on the website

pathCallbacks = os.environ['USERPROFILE']+'/Downloads/bokeh_flask/bokeh_flask_vm/static/js/callbacks/'
    
def checkbox(source, source2_respaldo, source_respaldo, oculta_zonas): 
    """
        Esta funcion recibe como parametros el source original y uno de respaldo para poder recordar
        las posiciones en x, luego lo que hace es llenar todas las posiciones en x en NaN's. En caso de lo que se haga
        sea mostrar las zonas, rellena con los antiguos valores en x mediante el source de respaldo.
    """
    fileO = open(pathCallbacks + 'checkbox.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_checkbox = CustomJS(args = {'source': source, 'source2': source2_respaldo, 'source_respaldo': source_respaldo, 'labs' : oculta_zonas},
        code = code)
    return callback_checkbox

def guarda_zona(source3):
    """
        Este callback sirve solamente para el select, el cual ayuda a 'recordar' la zona que se modifica.
    """
    fileO = open(pathCallbacks + 'guarda_zona.js', 'r')
    code = fileO.read()
    fileO.close()
    guarda_zona = CustomJS(args = {'source3': source3}, 
        code = code)
    return guarda_zona

def evento(source, source3, source_respaldo, source_cuadrados):
    """
        En esta funcion se recorre el checkbox de los eventos para determinar cuales son los activos, y en base a eso
        modifica el source original para poder asignar los nuevos eventos permitidos en la zona a modificar.
        Se le asigna un color (naranja) si la zona permite eventos, si no los permite, se le asigna otro color (gris)
        simbolizando la zona silenciada.
    """
    fileO = open(pathCallbacks + 'eventos_perm.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_evento = CustomJS(args = {'source': source, 'source3' : source3, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados},
        code = code)
    return callback_evento

def intensidad(source, source3, source_respaldo):
    """
        Mediante esta funcion se toma el valor actual del slider cada vez que se lo modifica para así ir modificando
        en tiempo real la intensidad relativa de la zona a modificar.
    """
    fileO = open(pathCallbacks + 'intensidad_rel.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_int = CustomJS(args = {'source': source, 'source3' : source3, 'source_respaldo': source_respaldo},
        code = code)
    return callback_int

def deshace_cambios(source, source_respaldo, source_cuadrados, input_eventos, slider_intensidad, eventos_perm, source3, poly_draw_tool):
    """                
        Esta funcion como propósito tiene el poder volver al último cambio realizado, tanto en movimiento de zonas como
        en cambio de eventos permitidos e intensidad relativa.
        
            Por el momento lo que hace es volver a la intensidad
        relativa anterior y a los últimos eventos modificados, y elimina líneas creadas a partir de la herramienta
        que permite mover zonas. Falta agregar que pueda volver la última zona modificada
        a su posición anterior.
    """
    fileO = open(pathCallbacks + 'deshace_cambios.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_deshace_cambios = CustomJS(args = {'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados,
                                                'eventos_perm': eventos_perm, 'eventos':input_eventos, 'slider': slider_intensidad, 'source3' : source3, 'poly_draw_tool': poly_draw_tool},
        code = code)
        
    return callback_deshace_cambios
    
def download(source):
    """
        Recibe como parámetro el source que contiene todos los datos de las zonas, lo transforma en un string largo,
        el cual se forma concatenando cada fila con un salto de línea y cada columna con una coma.
        Esto generada un archivo '.csv' en el navegador que se descarga desde el mismo.
        En la próxima carga de la página principal del mapa, este archivo sirve como nuevos parámetros para el mapa.
    """
    
    fileO = open(pathCallbacks + 'download.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_download = CustomJS(args={'source': source},
        code = code)
    return callback_download

def mouse_drag(source, source_cuadrados, source3, select, poli, slider_intensidad, input_eventos, eventos_perm, source_respaldo, largo_ducto):
    """
        En esta función se detectan los cambios en x de cada zona y las va modificando en tiempo real, evitando que
        quede alguna zona colgada.
        Toma todos los datos del source original y del source del sombreado de las zonas y los va comparando sobre la
        modificación en tiempo real para que vayan a la par.
        A su vez modifica la progresiva en base a la posición en x de cada zona.
        También muestra la zona que se está seleccionando y modificando en ese momento.
    """
    fileO = open(pathCallbacks + 'mouse_drag.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_mouse = CustomJS(args={'source': source, 'source_cuadrados':source_cuadrados, 'source3': source3, 'select': select, 'poli': poli,
                                    'slider': slider_intensidad, 'eventos': input_eventos, 'eventos_perm': eventos_perm, 'source_respaldo': source_respaldo, 'largo_ducto': largo_ducto}, 
            code = code)
    return callback_mouse

def mouse_end(poli, source_cuadrados, source, largo_ducto, draw_tool_l1, boton_elimina_zona, source_respaldo):
    """
        Esta función lo único que hace es detectar cuando el mouse deja de estar realizando cambios sobre la figura
        y deja de mostrar la zona activa, además de que desactiva la herramienta que sirve para modificar las zonas.
    """
    fileO = open(pathCallbacks + 'mouse_end.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_mouse_end = CustomJS(args={'poli': poli, 'source_cuadrados': source_cuadrados, 'source': source, 'largo_ducto': largo_ducto, 'draw_tool_l1': draw_tool_l1, 'boton_elimina_zona': boton_elimina_zona, 'source_respaldo': source_respaldo}, 
            code = code)
    return callback_mouse_end

def mouse_move(source, source_respaldo, source_cuadrados):
    """
        Esta función se creó con el fin de que por más que se quisiese mover una zona fuera de la figura, siempre
        mantenga sus coordenadas en y.
    """
    fileO = open(pathCallbacks + 'mouse_move.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_mouse_move = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados':source_cuadrados},
            code = code)
    return callback_mouse_move

def mouse_guarda(source, source_respaldo, source_cuadrados):
    """
        Función con el fin de poder guardar los datos de la antigua posición en x de cada zona para poder deshacer
        cambios. 
    """
    fileO = open(pathCallbacks + 'mouse_guarda.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_mouse_guarda = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados':source_cuadrados},
        code = code)
    return callback_mouse_guarda

def tap(source, source_respaldo, source3, source_cuadrados, slider_intensidad, input_eventos, eventos_perm, select, poli, draw_tool_l1, boton_elimina_zona, boton_muestra_eventos_zona, data_table, div2):
    """
        Detecta el click sobre la figura, determina las coordenadas en x correspondientes a la zona, actualiza el
        select de la zona automáticamente y los deshabilita mientras haya una zona seleccionada.
        
        Esta función habilita automáticamente la herramienta para modificar zonas.
    """
    fileO = open(pathCallbacks + 'tap.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_tap = CustomJS(args={'source': source, 'source3': source3,'source_cuadrados':source_cuadrados,'slider': slider_intensidad, 'eventos': input_eventos, 'eventos_perm': eventos_perm, 'select': select, 'poli': poli, 'draw_tool_l1': draw_tool_l1, 'boton_elimina_zona': boton_elimina_zona, 'source_respaldo': source_respaldo, 'boton_muestra_eventos_zona': boton_muestra_eventos_zona, 'data_table': data_table, 'div2': div2},
        code = code)
    return callback_tap

def muestra_eventos_zona(source, source_eventos, source_historicos_muestra, data_table, select, div2):
    """
        En esta función, siempre y cuando haya una zona seleccionada previamente, lo que se hace es mostrar los
        últimos 10 eventos correspondientes a las progresivas comprendidas en la zona seleccionada.
    """
    fileO = open(pathCallbacks + 'muestra_eventos_zona.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_muestra_eventos_zona = CustomJS(args={'source': source, 'source_eventos': source_eventos, 'source_historicos_muestra': source_historicos_muestra, 'dataTable': data_table, 'select': select, 'div2': div2},
        code = code)
    return callback_muestra_eventos_zona

def agrega_zona(text_input_prog_ini, text_input_prog_fin, boton_confirma_zona):
    """
        Esta función alterna entre labels de un botón que sirve para agregar zonas, el cual habilita dicha herramienta.
    """
    fileO = open(pathCallbacks + 'agrega_zona.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_agrega_zona = CustomJS(args={'text_input_prog_ini': text_input_prog_ini, 'text_input_prog_fin': text_input_prog_fin, 'boton_confirma_zona': boton_confirma_zona},
        code = code)
    return callback_agrega_zona

def confirma_zona(source, source_respaldo, source_cuadrados, select, text_input_prog_ini, text_input_prog_fin):
    """
        Toma las progresivas inicial y final donde se agregará la nueva zona. Cabe destacar que por cada división
        de zona que se escriba (inicial, final) se generan tres zonas.
        Además verifica si hay alguna zona existente ya entre las progresivas que se ingresan, en caso de existir,
        la elimina para agregar la nueva zona.
    """
    fileO = open(pathCallbacks + 'confirma_zona.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_confirma_zona = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados, 'select': select,'text_input_prog_ini': text_input_prog_ini, 'text_input_prog_fin': text_input_prog_fin},
        code = code)
    return callback_confirma_zona

def elimina_zona(source, select):
    """
        Esta es una función que lo que hace es, si hay una zona seleccionada, permite eliminarla en caso de que ya
        no sea necesaria y la elimina totalmente, tanto funcional como visualmente.
    """
    fileO = open(pathCallbacks + 'elimina_zona.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_elimina_zona = CustomJS(args={'source': source, 'select': select}, code = code)
    return callback_elimina_zona




def filtra_rango_pk(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es tomar los rangos de progresiva a filtrar y muestra solamente los eventos comprendidos en ese
        rango de progresivas. A su vez, las filtra en base a los demás filtros (fecha, estado, vehiculo).
    """    
    fileO = open(pathCallbacks + 'filtra_rango_pk.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_rango_pk = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros},
        code = code) 
    return callback_filtra_rango_pk

def filtra_vehiculos(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es mirar el checkbox y qué está seleccionado para poder filtrar en base a los vehiculos seleccionados. 
        A su vez, las filtra en base a los demás filtros (fecha, estado, progresiva).
    """    
    fileO = open(pathCallbacks + 'filtra_vehiculos.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_vehiculos = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros},
        code = code)
    return callback_filtra_vehiculos

def filtra_id(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Toma el id que se ingrese en el input y busca en el source de históricos todos los eventos que tengan el mismo
        id.
    """    
    fileO = open(pathCallbacks + 'filtra_id.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_id = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros},
        code = code)
    return callback_filtra_id

def filtra_estado(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es mirar el checkbox y qué está seleccionado para poder filtrar en base a los estados seleccionados. 
        A su vez, las filtra en base a los demás filtros (fecha, vehiculo, progresiva).
    """    
    fileO = open(pathCallbacks + 'filtra_estado.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_estado = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros},
        code=code)
    return callback_filtra_estado

def boton_sube(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonBaja):
    """
        Esta función sirve para la solapa de históricos.
        Esta función va agregando visualmente al cuadro de históricos de a 500 eventos, inicialmente sin eventos para
        visualizar.
    """    
    fileO = open(pathCallbacks + 'boton_sube.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_boton_sube = CustomJS(args={'source_historicos': source_historicos, 'source_todos_historicos': source_todos_historicos, 'sourceIteraHistoricos': sourceIteraHistoricos, 'data_table': data_table, 'botonBaja': botonBaja},
        code = code)
    return callback_boton_sube

def boton_baja(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonSube):
    """
        Esta función sirve para la solapa de históricos.
        Esta función va quitando visualmente al cuadro de históricos de a 500 eventos, inicialmente sin eventos para
        visualizar.
    """   
    fileO = open(pathCallbacks + 'boton_baja.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_boton_baja = CustomJS(args={'source_historicos': source_historicos, 'source_todos_historicos': source_todos_historicos, 'sourceIteraHistoricos': sourceIteraHistoricos, 'data_table': data_table, 'botonSube': botonSube},
        code = code)
    return callback_boton_baja

def filtra_fecha_ini(source_filtros):
    """
        Toma la fecha inicial a filtrar y la guarda para poder realizar el filtrado.
    """
    fileO = open(pathCallbacks + 'filtra_fecha_ini.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_fecha_ini = CustomJS(args={'source_filtros': source_filtros}, code = code)
    return callback_filtra_fecha_ini

def filtra_fecha_fin(source_filtros):
    """
        Toma la fecha final a filtrar y la guarda para poder realizar el filtrado.
    """
    fileO = open(pathCallbacks + 'filtra_fecha_fin.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_fecha_fin = CustomJS(args={'source_filtros': source_filtros}, code = code)
    return callback_filtra_fecha_fin

def filtra_fecha(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Toma el rango de fechas a filtrar y muestra los eventos comprendidos en ese rango de fechas.
        A su vez filtra en base a los demás parámetros de filtrado (progresiva, estado, vehiculo)
    """
    fileO = open(pathCallbacks + 'filtra_fecha.js', 'r')
    code = fileO.read()
    fileO.close()
    callback_filtra_fecha = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros},
        code = code)
    return callback_filtra_fecha

#def muestra_todos_eventos(source_cambia_paginas):
#    """
#        NO USADA/NO FUNCIONA CORRECTAMENTE.
#        
#        Función creada para alternar entre mapa e históricos, pero se reemplazó por otro método.
#    """
#    fileO = open(pathCallbacks + 'muestra_.js', 'r')
#    code = fileO.read()
#    fileO.close()
#    callback_muestra_eventos_zona = CustomJS(args={'source_cambia_paginas': source_cambia_paginas}, code="""
#            source_cambia_paginas.data.pagina[0] = 1;
#        """)
#    return callback_muestra_eventos_zona
