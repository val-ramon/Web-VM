var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];});
var nueva_data = source3.data;
var indice = source.data.Intensity_tip.indexOf(nueva_data.zona[0]);
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
source.data.Eventos_permitidos[indice] = (data.toString()).replace(/,/g, "/");
source.change.emit();
console.log("callback completed");