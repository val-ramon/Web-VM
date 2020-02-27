# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 03:58:56 2020

@author: ybl0550
"""

import pyodbc, time
import pickle, os

#login db
while True:
    time.sleep(180)
    sv="SWPLPGLPAPL07"
    db="Y-NTEGRO"
    uid="yntegro"
    pwd="Fibra2019"
    driver="ODBC Driver 17 for SQL Server" 
    tuple_cnx=(driver,sv,db,uid,pwd)
    cnxn_str='DRIVER={%s};SERVER=%s;DATABASE=%s;uid=%s;pwd=%s' % tuple_cnx
    print (cnxn_str)
    cnxn = pyodbc.connect(cnxn_str)
    
    #traer todos
    select_qry='SELECT * FROM dbo.Eventos'
    crs=cnxn.cursor() #mejor adentro de with cnxn.cursor() as crs:
    crs.execute(select_qry)
    try:
        os.remove('C:/Users/ybl0550/Downloads/bokeh_flask_ultimo/bokeh_flask_vm/static/config/db.db')
        print ('escribiendo archivo db...')
        for row in crs.fetchall():
            #print row imprime todos los campos
            fileO = open(os.environ['USERPROFILE']+'Downloads/bokeh_flask_ultimo/bokeh_flask_vm/static/config/db.db', 'a')
            pickle.dump(row, fileO)
            fileO.close()
        print ('finalizado.')
    except:
        pass
    cnxn.close()
