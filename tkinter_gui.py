# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 12:00:56 2019

@author: edomene
"""
import tkinter as Tk
from tkinter import filedialog
from tkinter import messagebox
import os


laser_tension  = 1.15
laser_duracion = 300
laser_frecuencia = 5000
temp_setpoint = 16.55
temp_setpoint_bl = 20
temp_seguidor_bl = -3


def gui_vars():

    
    global dic_tk_vars
        
        
    root = Tk.Tk()
    root.title('DAS System GUI')
    
    dic_tk_vars = {}

    dic_tk_vars['frecuencia_var'] = Tk.StringVar()
    
    
    dic_tk_vars['ancho_de_pulso_var'] = Tk.StringVar()
    
    dic_tk_vars['tension_laser_var'] = Tk.StringVar()
    
    
    dic_tk_vars['temp_set_laser_var'] = Tk.StringVar()
    
    dic_tk_vars['temp_set_bloque_var'] = Tk.StringVar()
    
    
    dic_tk_vars['temp_seg_bloque_var'] = Tk.StringVar()
    
    
    dic_tk_vars['temp_act_laser_var'] = Tk.StringVar()
    
    dic_tk_vars['temp_set1_laser_var'] = Tk.StringVar()
    
    
    dic_tk_vars['temp_act_bloque_var'] = Tk.StringVar()
    
    dic_tk_vars['temp_set1_bloque_var'] = Tk.StringVar()
    
    dic_tk_vars['tension_act_laser_var'] = Tk.StringVar()
    
    dic_tk_vars['corr_laser_var'] = Tk.StringVar()
    
    dic_tk_vars['corr_bloque_var'] = Tk.StringVar()
    
    dic_tk_vars['temp_amb1_var'] = Tk.StringVar()
    
    dic_tk_vars['temp_amb2_var'] = Tk.StringVar()
    
    dic_tk_vars['laser_onoff_var'] = Tk.IntVar()
    
    dic_tk_vars['tec_onoff_var'] = Tk.IntVar()
    
    dic_tk_vars['tec_onoff_bl_var'] = Tk.IntVar()
    
    dic_tk_vars['seg_onoff_bl_var'] = Tk.IntVar()
    
    dic_tk_vars['control_int_ext_var'] = Tk.IntVar()
    
    dic_tk_vars['flag_var'] = Tk.IntVar()
    
    dic_tk_vars['guardar_onoff_var'] = Tk.IntVar()
    
    dic_tk_vars['filename_path_mon_var'] = Tk.StringVar()
    
#    return root, frecuencia_var, ancho_de_pulso_var, tension_laser_var, temp_set_laser_var, temp_set_bloque_var, temp_seg_bloque_var, temp_act_laser_var, temp_set1_laser_var, temp_act_bloque_var, temp_set1_bloque_var, tension_act_laser_var, corr_laser_var, corr_bloque_var, temp_amb1_var, temp_amb2_var, laser_onoff_var, tec_onoff_var, tec_onoff_bl_var, seg_onoff_bl_var, control_int_ext_var, flag_var, guardar_onoff_var, filename_path_mon_var
    return root, dic_tk_vars


def gui_config(root):
    global dic_tk_vars
    
    def callback_laser_onoff(*args):
        if dic_tk_vars['laser_onoff_var'].get() == 0:
            dic_tk_vars['laser_onoff_var'].set(1)
            laser_onoff_boton.config(fg='red')
            laser_onoff_boton['text'] = 'OFF '
        else:
            dic_tk_vars['laser_onoff_var'].set(0)
            laser_onoff_boton.config(fg='green')
            laser_onoff_boton['text'] = 'ON'
    
    
    def callback_tec_onoff(*args):
        if dic_tk_vars['tec_onoff_var'].get() == 0:
            dic_tk_vars['tec_onoff_var'].set(1)
            tec_onoff_boton.config(fg='red')
            tec_onoff_boton['text'] = 'OFF'
        else:
            dic_tk_vars['tec_onoff_var'].set(0)
            tec_onoff_boton.config(fg='green')  
            tec_onoff_boton['text'] = 'ON '
    
    def callback_tec_onoff_bl(*args):
        if dic_tk_vars['tec_onoff_bl_var'].get() == 0:
            dic_tk_vars['tec_onoff_bl_var'].set(1)
            tec_onoff_boton_bl.config(fg='red')
            tec_onoff_boton_bl['text'] = 'OFF'
        else:
            dic_tk_vars['tec_onoff_bl_var'].set(0)
            tec_onoff_boton_bl.config(fg='green')  
            tec_onoff_boton_bl['text'] = 'ON '		
    
    def callback_seg_onoff_bl(*args):
        if dic_tk_vars['seg_onoff_bl_var'].get() == 1:
            dic_tk_vars['seg_onoff_bl_var'].set(0)
            seg_onoff_boton_bl.config(fg='red')
            seg_onoff_boton_bl['text'] = 'OFF'
        else:
            dic_tk_vars['seg_onoff_bl_var'].set(1)
            seg_onoff_boton_bl.config(fg='green')  
            seg_onoff_boton_bl['text'] = 'ON '		
    
    
    def callback_control_intext(*args):
        if dic_tk_vars['control_int_ext_var'].get() == 0:
            dic_tk_vars['control_int_ext_var'].set(1)
            control_intext_boton['text'] = 'EXT'
            dic_tk_vars['flag_var'].set(1)
        else:
            dic_tk_vars['control_int_ext_var'].set(0)
            dic_tk_vars['flag_var'].set(0)
            control_intext_boton['text'] = 'INT'			
    
    def callback_buscar(*args):
        global filename_path
        filename_path_var = Tk.StringVar()
        filename_path_w = Tk.Label(root, width=50, font = "Helvetica 10 bold", textvariable=filename_path_var)
        filename_path_w.grid(column=0,row=16,columnspan=4,sticky='W')
        filename_path = filedialog.askdirectory(parent=root,title='Choose a directory')         
        filename_path_var.set(filename_path)
    
    
    def callback_guardar(*args):
        global filename_path, filename_path_mon, filename_path_mon_var,file_mon, guardar_onoff, ind_arch
        
        if dic_tk_vars['guardar_onoff_var'].get() == 1:
            dic_tk_vars['guardar_onoff_var'].set(0)
            button_guardar.config(fg='red')
#            file_mon.close()
        else:
    #        filename_path = filedialog.askdirectory(parent=root,title='Choose a directory')
            
            try:
                filename_path
            except:
                filename_path = None
                
            if filename_path != None:
                dic_tk_vars['guardar_onoff_var'].set(1)
                button_guardar.config(fg='green')
                j = 0
                while 1:
                    filename_path_mon = os.path.join(filename_path, 'MONITOREO_' + '%02d' % (j))
                    if not os.path.isdir(filename_path_mon):
                        break
                    j = j + 1
            
            #filename_path_mon = os.path.join(filename_path, 'MONITOREO')
                button_guardar_var.set(filename_path_mon)
                os.mkdir(filename_path_mon)    
                ind_arch = 0
                inttostr = '%06d' % (ind_arch)
                file_mon = open(os.path.join(filename_path_mon,inttostr + '.val' ),'w')
                dic_tk_vars['filename_path_mon_var'].set(filename_path_mon+"/"+inttostr + '.val' )
                file_mon.write('hora, control_ext, frecuencia_laser[Hz], ancho_de_pulso[ns], tec_laser_onoff, temp_act_laser[C], temp_set_laser[C], temp_set_laser1[C], tec_bloque_onoff, temp_act_bloque[C], temp_set_bloque[C], temp_set_bloque1[C], temp_seguidor_bloque[C],  modo_seguidor_bloque, tension_laser_act[mV], tension_laser_set[mV], temp_amb1[C], temp_amb2[C],corriente_tec_laser[mA], corriente_tec_bloque[mA] \n')
                file_mon.close()
            else:
                messagebox.showerror('Error', "Falta directorio de guardado. Presione 'BUSCAR' para seleccionarlo.")
    
    def callback_iniciar_sistema(*args):
        filename_path_sistema_var = Tk.StringVar()
        filename_path_sistema_var_l = Tk.Label(root, width=50, font = "Helvetica 10 bold", textvariable=filename_path_sistema_var)
        filename_path_sistema_var_l.grid(column=1,row=17,columnspan=4,sticky='W')
        filename_path_sistema = filedialog.askopenfilename(parent=root,title='Choose a file to run')         
        filename_path_sistema_var.set(filename_path_sistema)
#        print (subprocess.Popen(filename_path_sistema))
#        subprocess.Popen(filename_path_sistema, shell = True)
        das_name = filename_path_sistema.split('/')[-1]
#        print (das_name)
        os.system("start cmd /k " + das_name)
    #    das_thread=threading.Thread(target=das_open_thread)
    #    das_thread.setDaemon(True)
    #    das_thread.start()
    if dic_tk_vars['control_int_ext_var'].get() == 1:
        control_intext_boton = Tk.Button(root, text="EXT", font = "Helvetica 16 bold", command=callback_control_intext)
    else:
        control_intext_boton = Tk.Button(root, text="INT", font = "Helvetica 16 bold", command=callback_control_intext)
    
#    if control_int_ext_var.get() == 1:
#        control_intext_boton['text'] = 'EXT'
#    else:
#        control_intext_boton['text'] = 'INT'
        
    control_intext_boton.grid(column=3,row=0)
    control_l=Tk.Label(root,text="Control: ", font = "Helvetica 18 bold",)
    control_l.grid(column=0,row=0,sticky='W')
    control_l=Tk.Label(root,text="ns", font = "Helvetica 18 bold",)
    
    
    frecuencia_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['frecuencia_var'])
    frecuencia_w.grid(column=1,row=1,sticky='W')
    frecuencia_l=Tk.Label(root,text="Frecuencia: ", font = "Helvetica 18 bold",)
    frecuencia_l.grid(column=0,row=1,sticky='W')
    frecuencia_l=Tk.Label(root,text="Hz", font = "Helvetica 18 bold",)
    frecuencia_l.grid(column=2,row=1,sticky='W')
    dic_tk_vars['frecuencia_var'].set(laser_frecuencia)
    
    ancho_de_pulso_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['ancho_de_pulso_var'])
    ancho_de_pulso_w.grid(column=1,row=2,sticky='W')
    ancho_de_pulso_l=Tk.Label(root,text="Ancho de pulso: ", font = "Helvetica 18 bold",)
    ancho_de_pulso_l.grid(column=0,row=2,sticky='W')
    ancho_de_pulso_l=Tk.Label(root,text="ns", font = "Helvetica 18 bold",)
    ancho_de_pulso_l.grid(column=2,row=2,sticky='W')
    dic_tk_vars['ancho_de_pulso_var'].set(laser_duracion)
    
    tension_laser_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['tension_laser_var'])
    tension_laser_w.grid(column=1,row=3,sticky='W')
    tension_laser_l=Tk.Label(root,text=u"Tensión láser: ", font = "Helvetica 18 bold",)
    tension_laser_l.grid(column=0,row=3,sticky='W')
    tension_laser_l=Tk.Label(root,text="V", font = "Helvetica 18 bold",)
    tension_laser_l.grid(column=2,row=3,sticky='W')
    dic_tk_vars['tension_laser_var'].set(laser_tension)
    
    laser_onoff_boton = Tk.Button(root, text="OFF", font = "Helvetica 16 bold", command=callback_laser_onoff)
    laser_onoff_boton.grid(column=3,row=3)
    laser_onoff_boton.config(fg='red')
    
    temp_set_laser_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_set_laser_var'])
    temp_set_laser_w.grid(column=1,row=4,sticky='W')
    temp_set_laser_l=Tk.Label(root,text=u"Temperatura set láser: ", font = "Helvetica 18 bold",)
    temp_set_laser_l.grid(column=0,row=4,sticky='W')
    temp_set_laser_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_set_laser_l.grid(column=2,row=4,sticky='W')
    dic_tk_vars['temp_set_laser_var'].set(temp_setpoint)
    
    tec_onoff_boton = Tk.Button(root, text="OFF", font = "Helvetica 16 bold", command=callback_tec_onoff)
    tec_onoff_boton.grid(column=3,row=4)
    tec_onoff_boton.config(fg='red')
    
    temp_set_bloque_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_set_bloque_var'])
    temp_set_bloque_w.grid(column=1,row=5,sticky='W')
    temp_set_bloque_l=Tk.Label(root,text=u"Temperatura set bloque: ", font = "Helvetica 18 bold",)
    temp_set_bloque_l.grid(column=0,row=5,sticky='W')
    temp_set_bloque_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_set_bloque_l.grid(column=2,row=5,sticky='W')
    dic_tk_vars['temp_set_bloque_var'].set(temp_setpoint_bl)
    
    tec_onoff_boton_bl = Tk.Button(root, text="OFF", font = "Helvetica 16 bold", command=callback_tec_onoff_bl)
    tec_onoff_boton_bl.grid(column=3,row=5)
    tec_onoff_boton_bl.config(fg='red')
    
    temp_seg_bloque_w = Tk.Entry(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_seg_bloque_var'])
    temp_seg_bloque_w.grid(column=1,row=6,sticky='W')
    temp_seg_bloque_l=Tk.Label(root,text=u"Temperatura seguidor bloque: ", font = "Helvetica 18 bold",)
    temp_seg_bloque_l.grid(column=0,row=6,sticky='W')
    temp_seg_bloque_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_seg_bloque_l.grid(column=2,row=6,sticky='W')
    dic_tk_vars['temp_seg_bloque_var'].set(temp_seguidor_bl)
    
    seg_onoff_boton_bl = Tk.Button(root, text="OFF", font = "Helvetica 16 bold", command=callback_seg_onoff_bl)
    seg_onoff_boton_bl.grid(column=3,row=6)
    seg_onoff_boton_bl.config(fg='red')
    
    temp_act_laser_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_act_laser_var'])
    temp_act_laser_w.grid(column=1,row=7,sticky='W')
    temp_act_laser_l=Tk.Label(root,text=u"Temperatura actual láser: ", font = "Helvetica 18 bold",)
    temp_act_laser_l.grid(column=0,row=7,sticky='W')
    temp_act_laser_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_act_laser_l.grid(column=2,row=7,sticky='W')
    dic_tk_vars['temp_act_laser_var'].set(0.0)
    
    temp_set1_laser_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_set1_laser_var'])
    temp_set1_laser_w.grid(column=3,row=7,sticky='W')
    temp_set1_laser_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_set1_laser_l.grid(column=4,row=7,sticky='W')
    dic_tk_vars['temp_set1_laser_var'].set(0.0)
    
    temp_act_bloque_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_act_bloque_var'])
    temp_act_bloque_w.grid(column=1,row=8,sticky='W')
    temp_act_bloque_l=Tk.Label(root,text=u"Temperatura actual bloque: ", font = "Helvetica 18 bold",)
    temp_act_bloque_l.grid(column=0,row=8,sticky='W')
    temp_act_bloque_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_act_bloque_l.grid(column=2,row=8,sticky='W')
    dic_tk_vars['temp_act_bloque_var'].set(0.0)
    
    temp_set1_bloque_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_set1_bloque_var'])
    temp_set1_bloque_w.grid(column=3,row=8,sticky='W')
    temp_set1_bloque_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_set1_bloque_l.grid(column=4,row=8,sticky='W')
    dic_tk_vars['temp_set1_bloque_var'].set(0.0)
    
    tension_act_laser_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['tension_act_laser_var'])
    tension_act_laser_w.grid(column=1,row=9,sticky='W')
    tension_act_laser_l=Tk.Label(root,text=u"Tensión actual láser: ", font = "Helvetica 18 bold",)
    tension_act_laser_l.grid(column=0,row=9,sticky='W')
    tension_act_laser_l=Tk.Label(root,text="mV", font = "Helvetica 18 bold",)
    tension_act_laser_l.grid(column=2,row=9,sticky='W')
    dic_tk_vars['tension_act_laser_var'].set(0.0)
    
    corr_laser_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['corr_laser_var'])
    corr_laser_w.grid(column=1,row=10,sticky='W')
    corr_laser_l=Tk.Label(root,text=u"Corriente TEC láser: ", font = "Helvetica 18 bold",)
    corr_laser_l.grid(column=0,row=10,sticky='W')
    corr_laser_l=Tk.Label(root,text=" mA", font = "Helvetica 18 bold",)
    corr_laser_l.grid(column=2,row=10,sticky='W')
    dic_tk_vars['corr_laser_var'].set(0.0)
    
    corr_bloque_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['corr_bloque_var'])
    corr_bloque_w.grid(column=1,row=11,sticky='W')
    corr_bloque_l=Tk.Label(root,text=u"Corriente TEC bloque: ", font = "Helvetica 18 bold",)
    corr_bloque_l.grid(column=0,row=11,sticky='W')
    corr_bloque_l=Tk.Label(root,text=" mA", font = "Helvetica 18 bold",)
    corr_bloque_l.grid(column=2,row=11,sticky='W')
    dic_tk_vars['corr_bloque_var'].set(0.0)
    
    temp_amb1_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_amb1_var'])
    temp_amb1_w.grid(column=1,row=12,sticky='W')
    temp_amb1_l=Tk.Label(root,text=u"Temperatura ambiente1: ", font = "Helvetica 18 bold",)
    temp_amb1_l.grid(column=0,row=12,sticky='W')
    temp_amb1_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_amb1_l.grid(column=2,row=12,sticky='W')
    dic_tk_vars['temp_amb1_var'].set(0.0)
    
    
    temp_amb2_w = Tk.Label(root, width=7, font = "Helvetica 18 bold", textvariable=dic_tk_vars['temp_amb2_var'])
    temp_amb2_w.grid(column=1,row=13,sticky='W')
    temp_amb2_l=Tk.Label(root,text=u"Temperatura ambiente2: ", font = "Helvetica 18 bold",)
    temp_amb2_l.grid(column=0,row=13,sticky='W')
    temp_amb2_l=Tk.Label(root,text="°C", font = "Helvetica 18 bold",)
    temp_amb2_l.grid(column=2,row=13,sticky='W')
    dic_tk_vars['temp_amb2_var'].set(0.0)
    
    button_buscar = Tk.Button(root,text=u"Buscar", font = "Helvetica 16 bold", command=callback_buscar)
    button_buscar.grid(column=0,row=14,sticky='W')    
    
    
    button_guardar = Tk.Button(root,text=u"Guardar", font = "Helvetica 16 bold", command=callback_guardar)
    button_guardar.grid(column=0,row=15,sticky='W')   
    button_guardar.config(fg='red')
    
    button_guardar_var = Tk.StringVar()
    button_guardar_l=Tk.Label(root,font = "Helvetica 10 bold",textvariable=button_guardar_var)
    button_guardar_l.grid(column=0,row=17,columnspan=4,sticky='W')
    
    button_inicia_sistema = Tk.Button(root,text=u"Iniciar Sistema", font = "Helvetica 16 bold", command=callback_iniciar_sistema)
    button_inicia_sistema.grid(column=1,row=15,sticky='W')   
    button_inicia_sistema.config(fg='blue')
    
    dic_tk_vars['laser_onoff_var'].set(1)
    dic_tk_vars['tec_onoff_var'].set(1)
    dic_tk_vars['tec_onoff_bl_var'].set(1)
    dic_tk_vars['seg_onoff_bl_var'].set(0)
    dic_tk_vars['control_int_ext_var'].set(1)
    dic_tk_vars['flag_var'].set(0)
    dic_tk_vars['guardar_onoff_var'].set(0)
    
    root.mainloop()