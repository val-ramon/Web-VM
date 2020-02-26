# App web de VM

# La app funciona con Flask y Bokeh.

Lo que hace en renderizar figuras creadas con Bokeh y las embebe en Flask para poder verlas en formato web. Algunas cosas de Bokeh funcionan con código en javascript ya que Flask funciona con el motor jinja, lo cual lo hace una app web.

Se necesita obligatoriamente contar con un archivo '.csv' que cuente con las zonas a cargar en el mapa y un archivo '.db' que sea de la base de datos. 

Además se debe contar con versiones de 'osciloscopio.py' e 'impar.py' modificadas que se encuentran en VM que guardan las imágenes para el estado del equipo.

Es necesario que las carpetas '/static/estado' y '/static/wf' estén vacías ya que los programas realizan por sí solos las acciones con las imágenes

La app, al ejecutarse con la terminal, permite el acceso mediante la ip y el puerto a cualquier persona que se encuentre en la misma red.
Al ingresar la ip y puerto en un navegador (cualquiera menos IE), se accede a la página, mostrando como índice la solapa del mapa en caso de que no hubiese ningún usuario activo, y, en caso de que lo hubiese, se le muestra al usuario una página indicándole al mismo que ya existe alguien activo. A su vez, se está trabajando para que existan dos vistas del mapa, la vista de un usuario autorizado que pueda modificar el mapa y la vista del usuario que no pueda realizar cambios. La posibilidad de modificar el mapa implica modificar el ancho de las zonas, los eventos permitidos, la intensidad relativa, etc.
Además la página cuenta con otras tres solapas: Históricos, Estado del sistema y Waterfall.
En la solapa de Históricos, se carga la Base de Datos de todos los históricos, permitiéndole al usuario filtrar sobre la misma con distintos filtros (fecha, estado, progresiva, vehículo e id).
En la solapa de Estado del Sistema se le muestra al usuario dos imágenes, una correspondiente a la señal que representa el wf y la otra con las distintas relaciones snr del láser y del edfa.
Por último, en la solapa Waterfall, el usuario puede visualizar, cada 30 segundos, el último estado del Waterfall, el cual es tomado como captura del equipo.

Luego, si el usuario decide no realizar cambios, existe un botón que le permite desconectarse, con la posibilidad de reconectarse desde ahí mismo. En caso de que el usuario estuviese inactivo por más de 5 minutos, es desconectado automáticamente.
