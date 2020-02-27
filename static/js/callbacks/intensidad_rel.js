var s_data = source.data; // Toma la data que llega desde el source de Python y lo asigna a una variable
var data = cb_obj.value; // Se fija el valor del slider mediante cb_obj
var nueva_data = source3.data; // Toma el valor de la data del source que sirve como memoria para identificar zona a modificar
var indice = s_data.Intensity_tip.indexOf(nueva_data.zona[0]); // Se fija el incide de la zona que debe modificar y lo guarda

s_data.rel_int[indice] = data.toFixed(2); // Cuando encuentra el indice, asigna el nuevo valor de intensidad relativa al source original y lo redondea a dos decimales
source.change.emit(); // Aplica los cambios al source
console.log("callback completed");
