// Los sources llegan como parametros desde Python

var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];}); // Mapea los campos seleccionados en el checkbox de eventos permitidos
var nueva_data = source3.data; // Se fija en que zona debe modificar
var indice = source.data.Intensity_tip.indexOf(nueva_data.zona[0]); // Busca el indice de la zona a modificar

// Asigna el color del sombreado de la zona en base a los eventos permitidos
if (data.includes("Ninguno") && data.length === 1){
    source.data.color[indice] = "Gray";
    source_cuadrados.data.color[indice] = 'White';
}
if (data.length === 1 && !data.includes("Ninguno")){
    source.data.color[indice] = "Orange";
}
if (data.length === 2 && !data.includes("Ninguno")){
    source.data.color[indice] = "Orange";
}
if (data.length === 3 && !data.includes("Ninguno")){
    source.data.color[indice] = "Orange";
}
source.data.Eventos_permitidos[indice] = (data.toString()).replace(/,/g, "/"); // Asigna los eventos permitidos al source para mostrarlos al ver la zona
source.change.emit(); // Emite los cambios en el source
console.log("callback completed");
