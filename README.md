# vm-codes

# La app funciona con Flask y Bokeh.

# Lo que hace en renderizar figuras creadas con Bokeh y las embebe en Flask para poder verlas en formato web. Algunas cosas de Bokeh funcionan con código en javascript ya que Flask funciona con el motor jinja, lo cual lo hace una app web.

# Se necesita obligatoriamente contar con un archivo '.csv' que cuente con las zonas a cargar en el mapa y un archivo '.db' que sea de la base de datos. 

# Además se debe contar con versiones de 'osciloscopio.py' e 'impar.py' modificadas que se encuentran en VM que guardan las imágenes para el estado del equipo.

# A su vez en VM se encuentra un script que descarga la base de datos periódicamente.

# 'generador3.py' sirve para la traza de VM en Google Earth.

Es necesario que las carpetas '/static/estado' y '/static/wf' estén vacías ya que los programas realizan por sí solos las acciones con las imágenes
