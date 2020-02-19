# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:10:44 2019

@author: edomene
"""

import numpy as np
import struct
import time
import os
import datetime

dic_datos_ard = {}

#Se usan las siguientes dos variables para arreglar el error de medicion en la corriente
offset_corr_laser = 1020
offset_corr_bloque = 1090

laser_frecuencia_ant = 5000
laser_duracion_ant = 300
laser_tension_ant = 1.15
temp_setpoint_ant = 16.55
temp_setpoint_bl_ant = 20
temp_seguidor_bl_ant = -3

iter_cont = 5
iter_cont1 = 500
corriente_laser_tot = np.array([])
corriente_bloque_tot = np.array([])
temp_amb1_tot = np.array([])
temp_amb1_tot1 = np.array([])
temp_amb2_tot = np.array([])
temp_amb2_tot1 = np.array([])

temp_amb1_tot1_p = 24
temp_amb2_tot1_p = 24
cont = 0

start = datetime.datetime.now()
ind_med = 0
ind_arch = 0

control_int_ext = 0

    
def guardado_de_datos(dic_tk_vars, array_serial, dic_datos_ard, file_mon):
    global temp_amb1_tot_p, temp_amb2_tot_p, corriente_laser_tot_p, corriente_laser_tot_p
    global ind_med, ind_arch, control_int_ext
    
    mediciones_por_archivo = 2000
    
    tension_laser_act = array_serial[10]
    temp_setpoint1 = array_serial[9]
    temp_setpoint_bl1 = array_serial[7]
    temp_laser_actual = array_serial[8]
    temp_bloque_actual = array_serial[6]
    control_int_ext = int(array_serial[12])
    
    ind_med = ind_med + 1                    
    ind_med = ind_med%mediciones_por_archivo + 1

    if dic_datos_ard['tec_onoff'] == 0:
        tec_onoff_s = 1
    else:
        tec_onoff_s = 0
        
    if dic_datos_ard['tec_onoff_bl'] == 0:
        tec_onoff_bl_s = 1
    else:
        tec_onoff_bl_s = 0     
         
        
    tiempo_actual = datetime.datetime.now()
    data_string2 = str(tiempo_actual)+ ', ' + str(control_int_ext) + ', ' + str(dic_datos_ard['laser_frecuencia']) + ', ' + str(dic_datos_ard['laser_duracion']) + ', ' + str(tec_onoff_s) + ', ' + str(temp_laser_actual) + ', ' + str(dic_datos_ard['temp_setpoint'])  + ', ' + str(temp_setpoint1) + ', ' + str(tec_onoff_bl_s)  + ', ' + str(temp_bloque_actual) + ', ' + str(dic_datos_ard['temp_setpoint_bl']) + ', ' + str(temp_setpoint_bl1) + ', ' + str(dic_datos_ard['temp_seguidor_bl']) + ', ' + str(dic_datos_ard['seg_onoff_bl'])  + ', ' + str(tension_laser_act)  + ', ' + str(dic_datos_ard['laser_tension']*1000)  + ', ' + str(temp_amb1_tot_p) + ', ' + str(temp_amb2_tot_p)  + ', ' + str(corriente_laser_tot_p) + ', ' + str(corriente_laser_tot_p) + '\n'   

    if ind_med == mediciones_por_archivo:
        file_mon.close()
        filename_path_mon = dic_tk_vars['filename_path_mon_var'].get()[:-10]
        ind_arch = ind_arch + 1
        inttostr = '%06d' % (ind_arch)                        
        file_mon = open(os.path.join(filename_path_mon,inttostr + '.val' ),'w') 
        file_mon.write('hora, control_ext, frecuencia_laser[Hz], ancho_de_pulso[ns], tec_laser_onoff, temp_act_laser[C], temp_set_laser[C], temp_set_laser1[C], tec_bloque_onoff, temp_act_bloque[C], temp_set_bloque[C], temp_set_bloque1[C], temp_seguidor_bloque[C],  modo_seguidor_bloque, tension_laser_act[mV], tension_laser_set[mV], temp_amb1[C], temp_amb2[C], corriente_tec_laser[mA], corriente_tec_bloque[mA] \n')

    if not file_mon.closed: 
        print("guardando configuracion laser...")
        file_mon.write(data_string2)

    return file_mon
    

def lectura_arduino(arduino, dic_tk_vars):
    global temp_amb1_tot_p, temp_amb2_tot_p, corriente_laser_tot_p, corriente_laser_tot_p
    global cont, corriente_laser_tot, corriente_bloque_tot, temp_amb1_tot, temp_amb1_tot1, temp_amb2_tot, temp_amb2_tot1,temp_amb1_tot1_p,temp_amb2_tot1_p
    array_serial = 0
    a = arduino.read(1).decode('utf-8')
    b = arduino.read(1).decode('utf-8')

    if a.isdigit() and b == ',':

        rawString = arduino.readline()

        array_serial = np.fromstring(rawString, dtype=float, count=-1, sep=',')

        cantDatosEs13 = len(array_serial) == 13
        
        if cantDatosEs13:  
            cont = cont + 1
            tension_laser_act = array_serial[10]
            temp_setpoint1 = array_serial[9]
            temp_setpoint_bl1 = array_serial[7]
            temp_laser_actual = array_serial[8]
            temp_bloque_actual = array_serial[6]
            temp_amb1 = array_serial[0]
            temp_amb2 = array_serial[2]
            corriente_laser = array_serial[1]*1000 + offset_corr_laser
            corriente_bloque = array_serial[3]*1000 + offset_corr_bloque                                                    
            corriente_laser_tot = np.append(corriente_laser_tot,corriente_laser)
            corriente_bloque_tot = np.append(corriente_bloque_tot,corriente_bloque)
            temp_amb1_tot = np.append(temp_amb1_tot,temp_amb1)
            temp_amb1_tot1 = np.append(temp_amb1_tot1,temp_amb1)
            
            temp_amb2_tot = np.append(temp_amb2_tot,temp_amb2)
            temp_amb2_tot1 = np.append(temp_amb2_tot1,temp_amb2)  
                      
            if cont > iter_cont:
                corriente_laser_tot = np.delete(corriente_laser_tot,0)
                corriente_bloque_tot = np.delete(corriente_bloque_tot,0)
                temp_amb1_tot = np.delete(temp_amb1_tot,0)
                temp_amb2_tot = np.delete(temp_amb2_tot,0)
                
            if cont > iter_cont1:    
                temp_amb1_tot1 = np.delete(temp_amb1_tot1,0)
                temp_amb2_tot1 = np.delete(temp_amb2_tot1,0)
            
            corriente_laser_tot_p = np.mean(corriente_laser_tot)
            corriente_bloque_tot_p = np.mean(corriente_bloque_tot)
            temp_amb1_tot_p = np.mean(temp_amb1_tot)
            temp_amb1_tot1_p = np.mean(temp_amb1_tot1)
            
            temp_amb2_tot_p = np.mean(temp_amb2_tot)
            temp_amb2_tot1_p = np.mean(temp_amb2_tot1)
            
            
            dic_tk_vars['temp_act_laser_var'].set('% 6.3f' % temp_laser_actual)
            dic_tk_vars['temp_set1_laser_var'].set('% 6.3f' % temp_setpoint1)
            dic_tk_vars['temp_act_bloque_var'].set('% 6.3f' % temp_bloque_actual)
            dic_tk_vars['temp_set1_bloque_var'].set('% 6.3f' % temp_setpoint_bl1)
            dic_tk_vars['tension_act_laser_var'].set('% 6.2f' % tension_laser_act)
            dic_tk_vars['temp_amb1_var'].set('% 6.2f' % temp_amb1_tot_p)
            dic_tk_vars['temp_amb2_var'].set('% 6.2f' % temp_amb2_tot_p)
            dic_tk_vars['corr_laser_var'].set('% 6.2f' % corriente_laser_tot_p)
            dic_tk_vars['corr_bloque_var'].set('% 6.2f' % corriente_bloque_tot_p)
    
    return dic_tk_vars, array_serial
                
def escritura_arduino(arduino, dic_tk_vars):
    global laser_frecuencia_ant, laser_duracion_ant, laser_tension_ant, temp_setpoint_ant
    global temp_setpoint_bl_ant, temp_seguidor_bl_ant, control_int_ext, dic_datos_ard
    
    flag1 = 10
    
    try:
        dic_datos_ard['laser_frecuencia'] = float(dic_tk_vars['frecuencia_var'].get())
        dic_datos_ard['laser_duracion'] = float(dic_tk_vars['ancho_de_pulso_var'].get())
        dic_datos_ard['laser_tension'] = float(dic_tk_vars['tension_laser_var'].get())
        
    except:
        dic_datos_ard['laser_frecuencia'] = laser_frecuencia_ant
        dic_datos_ard['laser_duracion'] = laser_duracion_ant
        dic_datos_ard['laser_tension'] = laser_tension_ant
        
    laser_frecuencia_ant = dic_datos_ard['laser_frecuencia']
    laser_duracion_ant = dic_datos_ard['laser_duracion']
    laser_tension_ant = dic_datos_ard['laser_tension']
    
    try:
        dic_datos_ard['temp_setpoint'] = float(dic_tk_vars['temp_set_laser_var'].get())
        dic_datos_ard['temp_setpoint_bl'] = float(dic_tk_vars['temp_set_bloque_var'].get())
        dic_datos_ard['temp_seguidor_bl'] = float(dic_tk_vars['temp_seg_bloque_var'].get())
        
    except: 
        dic_datos_ard['temp_setpoint'] = temp_setpoint_ant
        dic_datos_ard['temp_setpoint_bl'] = temp_setpoint_bl_ant
        dic_datos_ard['temp_seguidor_bl'] = temp_seguidor_bl_ant
    
    temp_setpoint_ant = dic_datos_ard['temp_setpoint']
    temp_setpoint_bl_ant = dic_datos_ard['temp_setpoint_bl']
    temp_seguidor_bl_ant = dic_datos_ard['temp_seguidor_bl']
        
    dic_datos_ard['laser_onoff'] = dic_tk_vars['laser_onoff_var'].get()
    dic_datos_ard['tec_onoff'] = dic_tk_vars['tec_onoff_var'].get()
    dic_datos_ard['tec_onoff_bl'] = dic_tk_vars['tec_onoff_bl_var'].get()
    dic_datos_ard['seg_onoff_bl'] = dic_tk_vars['seg_onoff_bl_var'].get()
    dic_datos_ard['control_int_ext'] = dic_tk_vars['control_int_ext_var'].get()
    
    if dic_datos_ard['seg_onoff_bl'] == 1:
        dic_datos_ard['temp_setpoint_bl'] = temp_amb1_tot1_p + dic_datos_ard['temp_seguidor_bl']
    if dic_tk_vars['flag_var'].get() == 1:       
        print ('flag1 ini')
        for i in range(flag1):
            arduino.write(struct.pack('<bfffiififi',0,dic_datos_ard['laser_frecuencia'],dic_datos_ard['laser_duracion'],dic_datos_ard['laser_tension'],int(dic_datos_ard['laser_onoff']),int(dic_datos_ard['tec_onoff']),dic_datos_ard['temp_setpoint'],int(dic_datos_ard['tec_onoff_bl']),dic_datos_ard['temp_setpoint_bl'],int(dic_datos_ard['control_int_ext'])))
            arduino.flush()
            time.sleep(0.4)
#                    flag_var.set(0)     
        print ('flag1 fin')
    else:
        arduino.write(struct.pack('<bfffiififi',0,dic_datos_ard['laser_frecuencia'],dic_datos_ard['laser_duracion'],dic_datos_ard['laser_tension'],int(dic_datos_ard['laser_onoff']),int(dic_datos_ard['tec_onoff']),dic_datos_ard['temp_setpoint'],int(dic_datos_ard['tec_onoff_bl']),dic_datos_ard['temp_setpoint_bl'],int(dic_datos_ard['control_int_ext'])))    
    
    return dic_datos_ard
   
    
