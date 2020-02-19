# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 13:58:22 2016
@author: hh_s
"""

"""
A simple example of an animated plot
"""
import pandas as pd
import numpy as np
import win32file
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import seaborn
import sys
import datetime 

#print ("pipe adentro")


pipeExists = False


if pipeExists:
    fileHandle = win32file.CreateFile("\\\\.\\pipe\\Pipe3",
                                  win32file.GENERIC_READ,
                                  0, None,
                                  win32file.OPEN_EXISTING,
                                  0, None)
    
    #tam=10000
    bins=int(sys.argv[1])
    cant_curvas=int(sys.argv[2])
    qfrec=int(sys.argv[3])
    tam = bins*cant_curvas*2
    
else:
#    pipeExists = False
    bins = 22500
    cant_curvas = 10
    qfrec = 4
    tam = bins*cant_curvas*2

#print ("pipe adentro", tam)

lines0 = []
lines1 = []

mvg_avg_window = 300

binsToZoom = 22500
maxVoltage = 0.5

divData = (2**14)

fig,([ax0,ax1]) = plt.subplots(2,1)
fig.canvas.set_window_title('Osciloscopio')

#------------------ Grafico para canal 0
x0=np.random.uniform(0.05,0.1,size=(bins,1))
x00=np.random.uniform(0.05,0.1,size=(bins,1))
ax0 = plt.subplot2grid((2, 8), (0, 0), colspan=6)
for i in range(cant_curvas):
    lines0.append(ax0.plot(x0,color='b',linewidth=0.5,alpha=0.5))  
lines0.append(ax0.plot(x00,color='g',linewidth=1,alpha=1))     
lines0.append(ax0.plot(x00,color='k',linewidth=1,alpha=1))
    
ax0.grid(color='grey', linestyle='--', linewidth=0.5)
ax0.set_ylim([0, maxVoltage])
ax0.set_xlim([0, binsToZoom])

ax0.set_title(u'CH0')
ax0.set_ylabel(u'Tensión [V]')
ax0.set_xlabel(u'Bin')

#------------------- Grafico para canal 1
x1=np.random.uniform(0.05,0.1,size=(bins,1))
ax1 = plt.subplot2grid((2, 8), (1, 0), colspan=6)
for i in range(cant_curvas):
    lines1.append(ax1.plot(x1,color='r',linewidth=0.5,alpha=0.5))
ax1.grid(color='grey', linestyle='--', linewidth=0.5)
#ax1.set_ylim([0, maxVoltage])
#ax1.set_xlim([0, binsToZoom])

ax1.set_title(u'CH1')
ax1.set_ylabel(u'Tensión [V]')
ax1.set_xlabel(u'Bin')
ax1.set_ylim([0, 0.0016])
ax1.set_xlim([5, 45])


tiempo_actual = datetime.datetime.now()
time_str = datetime.datetime.strftime(tiempo_actual,'%Y-%m-%d %H:%M:%S')    
#print (time_str)
#tiempo_label.set_text(time_str)
t0 = ax0.text(1.02,1.1,'T:' + str(time_str),horizontalalignment='left', transform=ax0.transAxes, color='k')   

rango1 = []
rango2 = []

def animate(i):
    #line.set_ydata(x+i/100.0)  # update the data
    #return line,
   # if(i%15==0 and i>0):
       
    global rango1, rango2   
    
#    ax.plot(x+i/10.0,'.')
    if pipeExists:
        try:
            rr,rd = win32file.ReadFile(fileHandle,tam*4)
        except:
            sys.exit()
        
        datos = np.frombuffer(rd,dtype=np.float32)
        
    else:
        datos = np.random.normal(loc=10,scale=5, size=tam)
     
    ch0 = datos[0:int(tam/2)]
    ch1 = datos[int(tam/2):tam]
    
    ch0 = np.reshape(ch0,[cant_curvas,bins])
    ch1 = np.reshape(ch1,[cant_curvas,bins])
    
    ch0 = ch0/divData
    ch1 = ch1/divData
    
    for j in range(cant_curvas):
        lines0[j][0].set_ydata(ch0[j,:]) 
        lines1[j][0].set_ydata(ch1[j,:]) 
        
    ch0_mean = np.mean(ch0,axis=0)
    #ch0_mvg = np.convolve(ch0_mean,np.ones(mvg_avg_window)/mvg_avg_window,mode='valid')
    
    
    #cuenta rolling_mean con pandas>0.18
    
    ch0_mean_df=pd.DataFrame.from_records(ch0_mean.reshape(-1,1))#lo convierto a dataFrame para poder llamar .rolling      
    
    ch0_mvg = np.array(ch0_mean_df.rolling(mvg_avg_window,center=True).mean())
    ch0_std = np.array(ch0_mean_df.rolling(mvg_avg_window,center=True).std())
    
    ch0_std = ch0_std/ch0_mvg
    
#    print (ch0_mvg.shape)
    
    lines0[cant_curvas][0].set_ydata(ch0_mvg)     
    lines0[cant_curvas+1][0].set_ydata(ch0_std)
	
            
    tiempo_actual = datetime.datetime.now()
    time_str = datetime.datetime.strftime(tiempo_actual,'%Y-%m-%d %H:%M:%S')    
    t0.set_text('T:' + str(time_str))
    
#    ax0.plot(np.transpose(ch0),color='b',linewidth=0.5)
#    ax0.set_ylim([0,0.075])
#    
#    ax1.plot(np.transpose(ch1),color='b',linewidth=0.5)
#    ax1.set_ylim([0,0.025])
    
    return lines0, lines1,
    
    
    
    
        
#    ax.plot(xx1[0:yy1.size],yy1,'-')
#    ax.set_ylim([0,80])

#    ax2 = ax.twinx()
#    ax.plot(media_acc,color='b')
#    ax.set_xlim([0,199])
#    ax.set_ylim([0,15000])
    
#    ax2.plot(snr_acc,color='r')
#    ax2.set_ylim([0,300])

#    return line,


# Init only required for blitting to give a clean slate.

ani = animation.FuncAnimation(fig, animate,
                              interval=100, blit=False)
plt.show()