// Los sources los recibe desde Python como parametros

var s_data_respaldo = source_respaldo.data; // Toma la data del source de respaldo
var s_data_cuadrados = source_cuadrados.data; // Toma la data del source del sombreado de zonas
var s_data = source.data; // Toma la data del source que contiene la informacion de las zonas

// Esto sirve para poder hacer un respaldo de la data anterior de las zonas en caso de querer deshacer cambios
if(s_data_cuadrados.cont[0] === 0){
    s_data_cuadrados.cont[0] = 1;
    s_data_respaldo.rel_int = s_data.rel_int.slice();
    s_data_respaldo.Eventos_permitidos = s_data.Eventos_permitidos.slice();
    for (var i = 0; i < s_data_respaldo.length; i++){
        s_data_respaldo.RT[i].fill(s_data.RT[k][0]);
        s_data_respaldo.RT_intensity.fill(s_data.RT_intensity[k][0]);
    }
}
