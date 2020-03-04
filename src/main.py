# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:04:34 2020

@author: valramon
"""

from flask_app import *

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
    os.system("start cmd /k python mueve_archivo_cambios.py")
    os.system("start cmd /k python mueve_archivo_db.py")
#    os.system("start cmd /k python crea_archivo_db.py")
    app.run(port=5006, host='0.0.0.0')
