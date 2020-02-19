# -*- coding: utf-8 -*-
"""
Created on Thu Jan 04 09:17:11 2018

@author: Marco
"""

import time
import serial
import threading
from tkinter_gui import *
from arduino_functions import *

import warnings
import serial.tools.list_ports

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description  # may need tweaking to match new arduinos
]
if not arduino_ports:
#    raise IOError("No Arduino found")
    arduino_ports = ['COM3']
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

arduino = serial.Serial(arduino_ports[0], 9600, timeout=0.3)
archAbierto = 0
file_mon = 0


def data_update():
    global gui_abierta, dic_tk_vars, file_mon, archAbierto


    while gui_abierta:

        try:
            time.sleep(0.5)

            dic_datos_ard = escritura_arduino(arduino, dic_tk_vars)
            while arduino.inWaiting():
                dic_tk_vars, array_serial = lectura_arduino(arduino, dic_tk_vars)
                guardoDatos = dic_tk_vars['guardar_onoff_var'].get() == 1
#                  
                if guardoDatos:
                    if not archAbierto:
                        file_mon = open(dic_tk_vars['filename_path_mon_var'].get(), 'a')

                        archAbierto = 1
                    file_mon = guardado_de_datos(dic_tk_vars, array_serial, dic_datos_ard, file_mon)
                else:
                    file_mon.close()
                    archAbierto = 0
            while arduino.inWaiting() > 500:
                arduino.readline()
        except:
            pass
        
                            
gui_abierta = True


gui_thread=threading.Thread(target=data_update)
gui_thread.setDaemon(True)
gui_thread.start()


root, dic_tk_vars = gui_vars()

gui_config(root)

gui_abierta = False

gui_thread.join()

if archAbierto:

    file_mon.close()

arduino.close()

