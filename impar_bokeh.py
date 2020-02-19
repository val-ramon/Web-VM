# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 13:58:22 2016

@author: hh_s
"""

"""
A simple example of an animated plot
"""
import numpy as np
import win32file
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#import seaborn
import sys, os
import threading
import time

numberOfZeros = 200
pipeExists = False

if pipeExists:
    fileHandle = win32file.CreateFile("\\\\.\\pipe\\Pipe2",
                                  win32file.GENERIC_READ,
                                  0, None,
                                  win32file.OPEN_EXISTING,
                                  0, None)
    
    #tam=10000
    bin1=int(sys.argv[1])
    energia_size_laser=int(sys.argv[2])
    energia_size_edfa=int(sys.argv[3])
    bin_mon_laser_i = int(sys.argv[4])
    bin_mon_laser_f = int(sys.argv[5])
    bin_mon_edfa_i = int(sys.argv[6])
    bin_mon_edfa_f = int(sys.argv[7])
    cLASER = float(sys.argv[8])
    cEDFA = float(sys.argv[9])
    tam = bin1 + energia_size_laser + energia_size_edfa

else:
#    pipeExists = False
    bin1=43
    energia_size_laser=np.random.randint(40)
    energia_size_edfa=np.random.randint(40)
    bin_mon_laser_i = 20
    bin_mon_laser_f = 40
    bin_mon_edfa_i = 20
    bin_mon_edfa_f = 40
    cLASER = 2.01
    cEDFA = 2.01
    tam = bin1 + energia_size_laser + energia_size_edfa

#print ("pipe adentro", tam)

media_acc_edfa = np.ones(numberOfZeros) * numberOfZeros
snr_acc_edfa = np.ones(numberOfZeros) * numberOfZeros

media_acc_laser = np.ones(numberOfZeros) * numberOfZeros
snr_acc_laser = np.ones(numberOfZeros) * numberOfZeros

perfil_laser = np.ones(numberOfZeros*2) * numberOfZeros
perfil_edfa = np.ones(numberOfZeros*2) * numberOfZeros


fig,([ax1,ax2],[ax3,ax4]) = plt.subplots(2,2)
fig.canvas.set_window_title('Energia Laser - EDFA')
plt.rcParams["legend.loc"] = 'best'

#-------------------- Energia media laser - edfa

axMeanLaser = plt.subplot2grid((2, 8), (0, 0), colspan=4)
axMeanEdfa = axMeanLaser.twinx()

#-------------------- Relacion señal ruido laser - edfa
axSnrLaser = plt.subplot2grid((2, 8), (1, 0), colspan=4)
axSnrEdfa = axSnrLaser.twinx()
#-------------------- Potencia laser - edfa

axPotenciaLaser = plt.subplot2grid((2, 8), (0, 5), colspan=3)
axPotenciaEdfa = axPotenciaLaser.twinx()
#-------------------- Histograma laser - edfa

axHistLaser = plt.subplot2grid((2, 8), (1, 5), colspan=3)
axHistEdfa = axHistLaser.twiny()
     

lineMediaLaser,=axMeanLaser.plot(media_acc_laser,color='b')
lineMediaEdfa,=axMeanEdfa.plot(media_acc_edfa,color='r')
  

lineSnrLaser,=axSnrLaser.plot(snr_acc_laser,color='b')
lineSnrEdfa,=axSnrEdfa.plot(snr_acc_edfa,color='r')
       

linePotenciaLaser,=axPotenciaLaser.plot(perfil_laser,color='b')
linePotenciaEdfa,=axPotenciaEdfa.plot(perfil_edfa,color='r')

xToHist = np.random.uniform(-1,1,size=(500,1))
lineHistLaser, = axHistLaser.plot(xToHist,color='b')  
lineHistEdfa, = axHistEdfa.plot(xToHist,color='r')  

axMeanLaser.set_title('Energia media')
axMeanLaser.set_ylabel('Energia Laser [nJ]',color='b')
axMeanEdfa.set_ylabel('Energia EDFA [nJ]',color='r')
axMeanLaser.legend('Laser')    
axMeanEdfa.legend('EDFA')
axMeanLaser.set_ylim([0,10])
axMeanEdfa.set_ylim([0,100])

axSnrLaser.set_title('Energia SNR')
axSnrLaser.set_ylabel('SNR Energia Laser',color='b')
axSnrEdfa.set_ylabel('SNR Energia EDFA',color='r')
axSnrLaser.legend('Laser')    
axSnrEdfa.legend('EDFA')
axSnrEdfa.set_ylim([0,400]) 
axSnrLaser.set_ylim([0,400]) 

axPotenciaLaser.set_title('Perfil')
axPotenciaLaser.set_ylabel('Potencia Laser [W]',color='b')
axPotenciaEdfa.set_ylabel('Potencia EDFA [W]',color='r')
axPotenciaLaser.legend('Laser')    
axPotenciaEdfa.legend('EDFA')
axPotenciaLaser.set_xlim([0,200])
axPotenciaEdfa.set_xlim([0,200])
axPotenciaLaser.set_ylim([0,0.002])
axPotenciaEdfa.set_ylim([0,0.002])

axHistLaser.set_ylabel('Cuentas')
axHistLaser.set_xlabel('Energia Laser [nJ]',color='b')
axHistEdfa.set_xlabel('Energia EDFA [nJ]',color='r')
axHistLaser.legend('Laser')    
axHistEdfa.legend('EDFA')
axHistEdfa.set_xlim([0,0.1]) 
axHistLaser.set_xlim([0,0.1]) 
axHistLaser.set_ylim([0,10])
axHistEdfa.set_ylim([0,10])



rango1 = []
rango2 = []
i = 0

def animate(i, fig):
    #line.set_ydata(x+i/100.0)  # update the data
    #return line,
   # if(i%15==0 and i>0):
       
    global rango1, rango2, media_acc_laser, media_acc_edfa, snr_acc_laser, snr_acc_edfa
#    ax1.cla()
#    ax2.cla()
#    ax3.cla()
#    axHistLaser.cla()
#    ax11.cla()
#    ax22.cla()
#    ax33.cla()
#    axHistEdfa.cla()    
    while True:
        time.sleep(1)
#    ax.plot(x+i/10.0,'.')
        if pipeExists:
            try:
                rr,rd = win32file.ReadFile(fileHandle,tam*4)
            except:
                sys.exit()
            super_vector = np.frombuffer(rd,dtype=np.float32)
    
        else:
            super_vector = np.random.uniform(1, tam, size = tam)
            
        perfil = super_vector[0:(bin1-1)]  
        
        energia_laser = super_vector[bin1:(bin1+energia_size_laser-1)]    
        energia_edfa = super_vector[bin1+energia_size_laser:(bin1+energia_size_laser+energia_size_edfa-1)]  
        
        energia_laser = energia_laser*cLASER*2/pow(2,15)*5;
        energia_edfa = energia_edfa*cEDFA*2/pow(2,15)*5;
        
        perfil_laser[bin_mon_laser_i-2:bin_mon_laser_f+2] = cLASER*perfil[bin_mon_laser_i-2:bin_mon_laser_f+2]*2/pow(2,15)
        perfil_edfa[bin_mon_edfa_i-2:bin_mon_edfa_f+2] = cEDFA*perfil[bin_mon_edfa_i-2:bin_mon_edfa_f+2]*2/pow(2,15)
        
        
        media_laser = np.mean(energia_laser)
        std_laser = np.std(energia_laser)
        
        media_edfa = np.mean(energia_edfa)
        std_edfa = np.std(energia_edfa)    
        
    #    if (i%200==0): 
    #        
    #        media_acc = np.zeros(200)
        
        media_acc_laser = np.append(media_acc_laser, media_laser)
        snr_acc_laser = np.append(snr_acc_laser, (media_laser/std_laser))
        
        media_acc_laser = np.delete(media_acc_laser, 0)
        snr_acc_laser = np.delete(snr_acc_laser, 0)
        
        media_acc_edfa = np.append(media_acc_edfa, media_edfa)
        snr_acc_edfa = np.append(snr_acc_edfa, (media_edfa/std_edfa))
        
        media_acc_edfa = np.delete(media_acc_edfa, 0)
        snr_acc_edfa = np.delete(snr_acc_edfa, 0)
        
        if (i == 0):
            rango1 = np.array([media_laser-20*std_laser, media_laser+10*std_laser])
            rango2 = np.array([media_edfa-10*std_edfa, media_edfa+20*std_edfa])
            
            
        yy1_laser,xx1_laser = np.histogram(energia_laser,numberOfZeros,rango1)
        yy1_edfa,xx1_edfa = np.histogram(energia_edfa,numberOfZeros,rango2)
        
        lineMediaLaser.set_ydata(media_acc_laser)
        lineMediaEdfa.set_ydata(media_acc_edfa)
        
        lineSnrLaser.set_ydata(snr_acc_laser)
        lineSnrEdfa.set_ydata(snr_acc_edfa)
        
        linePotenciaLaser.set_ydata(perfil_laser)
        linePotenciaEdfa.set_ydata(perfil_edfa)
        
        lineHistLaser.set_data(xx1_laser[1::],yy1_laser)
        lineHistEdfa.set_data(xx1_edfa[1::],yy1_edfa)
        try:
            os.remove('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/estado/impar'+str(i - 2).zfill(10)+'.png')
        except:
            pass
        fig.savefig('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/estado/impar'+str(i).zfill(10)+'.png')
        i += 1
#   
#    ax1.plot(media_acc_laser,color='b')
#    
#    ax11.plot(media_acc_edfa,color='r')
#      
#
#    ax2.plot(snr_acc_laser,color='b')
#    
#    ax22.plot(snr_acc_edfa,color='r')
#           
#    
#    ax3.plot(perfil_laser,color='b')
#    ax33.plot(perfil_edfa,color='r')
      

#    axHistLaser.set_ylabel('Cuentas')
#    axHistLaser.set_xlabel('Energia Laser [nJ]',color='b')
#    axHistEdfa.set_xlabel('Energia EDFA [nJ]',color='r') 
#    axHistLaser.plot(xx1_laser[1::],yy1_laser,color='b')  
#    axHistEdfa.plot(xx1_edfa[1::],yy1_edfa,color='r')  


   
#    return lineMediaLaser, lineSnrLaser, linePotenciaLaser, lineHistLaser, lineMediaEdfa, lineSnrEdfa, linePotenciaEdfa, lineHistEdfa,
#horaAntigua = time.time()
#def saveFig():
#    global horaAntigua
#    while True:
#        horaActual = time.time()
#        if horaActual - horaAntigua >= 1:
#            fig.savefig('C:/Users/edomene/Downloads/bokeh_flask/bokeh_flask/static/prueba.png')
#            horaAntigua = horaActual
#   

#ani = animation.FuncAnimation(fig, animate,
#                              interval=500, blit=False)

#while True:
#    time.sleep(1)
#    fig.savefig('./prueba.png')

#plt.show()

saveFigThread = threading.Thread(target=animate, args=(i, fig))
saveFigThread.setDaemon(True)
saveFigThread.start()