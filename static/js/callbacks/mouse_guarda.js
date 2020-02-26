var s_data_respaldo = source_respaldo.data;
var s_data_cuadrados = source_cuadrados.data;
var s_data = source.data;
if(s_data_cuadrados.cont[0] === 0){
    s_data_cuadrados.cont[0] = 1;
    s_data_respaldo.rel_int = s_data.rel_int.slice();
    s_data_respaldo.Eventos_permitidos = s_data.Eventos_permitidos.slice();
    for (var i = 0; i < s_data_respaldo.length; i++){
        s_data_respaldo.RT[i].fill(s_data.RT[k][0]);
        s_data_respaldo.RT_intensity.fill(s_data.RT_intensity[k][0]);
    }
}