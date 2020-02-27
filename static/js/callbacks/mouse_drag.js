// Recibe los sources, el select y la herramienta mediante data pasada por parametro desde Python

var s_data = source.data; // Asigna la data del source en una variable
var s_data_cuadrados = source_cuadrados.data; // Asigna la data del source de sombreado a una variable
var largo = s_data_cuadrados.x.length; // Se fija cuantas zonas hay
var modifica = ''; // Crea una variable para saber la zona que debe dejar marcada y bloqueada en el select
var eve = []; // Crea un array para poder agregar los eventos permitidos y poder marcarlos en el checkbox


/* Recorre todas las zonas fijandose si hay algun cambio en las coordenadas en x de alguna zona y va modificando el sombreado en tiempo real,
    a su vez que bloquea el select y muestra la zona seleccionada con otro color*/
for (var i = 0; i < largo; i++){
    if (s_data_cuadrados.x[i][0][0][2] !== s_data.RT[i][0]){
        modifica = s_data.Intensity_tip[i];
        source3.data.zona[0] = modifica;
        s_data_cuadrados.color[i] = 'Red';
        select.value = modifica;
        poli.visible = true;
        for (var k = 0; k < eventos_perm.length; k++){
            if (s_data.Eventos_permitidos[i].includes(eventos_perm[k])){
                eve.push(k);
            }
        }
        eventos.active = eve;
        slider.value = s_data.rel_int[i];
    }
    s_data_cuadrados.x[i][0][0][2] = s_data.RT[i][0];
    s_data_cuadrados.x[i][0][0][3] = s_data.RT[i][0];
    var otro = i + 1;
    if (otro !== largo){
        s_data_cuadrados.x[otro][0][0][0] = s_data.RT[i][0];
        s_data_cuadrados.x[otro][0][0][1] = s_data.RT[i][0];
    }
    // Este if - else sirve para modificar las progresivas en tiempo real
    if (i === 0){
        s_data.ProgresivaIni[i] = 'pk338';
    }
    else{
        s_data.ProgresivaIni[i] = s_data.ProgresivaFin[i - 1];
    }
    var suma = (s_data.RT[i][0] - 510)/1000 + 338;
    s_data.ProgresivaFin[i] = 'pk' + ((suma.toFixed(2).toString()));
}

s_data.RT[largo - 1].fill(largo_ducto); // Rellena la ultima zona con la misma coordenada para forzar a que sea inamovible

// Aplica los cambios a los sources
source3.change.emit();
source.change.emit();
source_cuadrados.change.emit();
