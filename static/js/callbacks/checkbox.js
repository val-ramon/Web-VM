// Los sources los recibe como parametros desde Python

var s_data = source.data; // Toma la data del source original
var s_data_respaldo = source2.data; // Toma la data del source para respaldar las coordenadas en x
var select_vals = cb_obj.active.map(function(x){return cb_obj.labels[x];}); // Se fija si el checkbox esta seleccionado o no
var nan = NaN; // Crea una variable con NaN para poder ocultar las zonas

// Se guarda los valores de las coordenadas en x para tener una memoria de cuales eran los valores anteriores antes de ocultarlos
for (var i = 0; i < s_data_respaldo.x.length; i++){
    if(!isNaN(s_data.RT[i][0])){
        s_data_respaldo.x[i].fill(s_data.RT[i][0]);
    }
}

// Recorre todo el source y, en caso de que esten mostradas, las oculta rellenandolas con NaN's, caso contrario las rellena con valores anteriores para mostrar las zonas nuevamente
var x_respaldo = s_data.RT;
for (var i = 0; i < s_data.RT.length; i++) {
    if (!(select_vals.includes(labs[0]))){
        x_copia = s_data.RT.slice();
        s_data.RT[i].fill(nan);
        s_data.RT_intensity[i].fill(nan);
    }
    else{
        if (isNaN(x_respaldo[i][0])){
            s_data.RT[i].fill(s_data_respaldo.x[i][0]);
        }
        else{
            s_data.RT[i].fill(x_respaldo[i][0]);
        }
        s_data.RT_intensity[i] = [];
        for (var j = 0; j < 50; j++){
            s_data.RT_intensity[i].push(j);
        }
    }
}
source_respaldo = source; // Hace un respaldo de todo el source original
source.change.emit(); // Emite los cambios
console.log("callback completed");
