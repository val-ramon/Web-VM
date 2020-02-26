var s_data_cuadrados = source_cuadrados.data;
var eve = [];
var s_data_respaldo = source_respaldo.data;
var s_data = source.data;
var contNulls = 0;
for (var i = 0; i < s_data.Intensity_tip.length; i++){
    var veoUltimo = s_data.Intensity_tip[i];
    if (veoUltimo === null){
        contNulls++;
    }
}
if (contNulls > 0){
    for (var i = 0; i < contNulls; i++){
        s_data.Eventos_permitidos.pop();
        s_data.RT.pop();
        s_data.RT_intensity.pop();
        s_data.index.pop();
        s_data.color.pop();
        s_data.Intensity_tip.pop();
        s_data.rel_int.pop();
        s_data.ProgresivaIni.pop();
        s_data.ProgresivaFin.pop();
    }
}
else {
    for (var i = 0; i < s_data_respaldo.length; i++){
        s_data.RT[i].fill(s_data_respaldo.RT[k][0]);
        s_data.RT_intensity.fill(s_data_respaldo.RT_intensity[k][0]);
    }
    s_data.Eventos_permitidos = s_data_respaldo.Eventos_permitidos.slice();
    s_data.index = s_data_respaldo.index.slice();
    s_data.color = s_data_respaldo.color.slice();
    s_data.Intensity_tip = s_data_respaldo.Intensity_tip.slice();
    s_data.rel_int = s_data_respaldo.rel_int.slice();
    s_data.ProgresivaIni = s_data_respaldo.ProgresivaIni.slice();
    s_data.ProgresivaFin = s_data_respaldo.ProgresivaFin.slice();
    s_data_respaldo.RT = s_data.RT.slice();
    s_data_respaldo.RT_intensity = s_data.RT_intensity.slice();
}
var largo = s_data_cuadrados.x.length;
for (var i = 0; i < largo; i++){
    s_data_cuadrados.x[i][0][0][2] = s_data.RT[i][0];
    s_data_cuadrados.x[i][0][0][3] = s_data.RT[i][0];
    var otro = i + 1;
    if (s_data.Eventos_permitidos[i].includes('Ninguno')){
        s_data_cuadrados.color[i] = 'White';
    }
    else{
        s_data_cuadrados.color[i] = 'Grey';
    }
    if (otro !== largo){
        s_data_cuadrados.x[otro][0][0][0] = s_data.RT[i][0];
        s_data_cuadrados.x[otro][0][0][1] = s_data.RT[i][0];
    }
}
var indice = s_data.Intensity_tip.indexOf(source3.data.zona[0]);
for (var k = 0; k < eventos_perm.length; k++){
    if (s_data.Eventos_permitidos[indice].includes(eventos_perm[k])){
        eve.push(k);
    }
}
poly_draw_tool.active = false;
function range(start, end) {
    var ans = [];
    for (let i = start; i <= end; i++) {
        ans.push(i);
    }
    return ans;
} 
s_data.RT_intensity[s_data.RT_intensity.length - 1] = range(0, 49);
eventos.active = eve;
slider.value = s_data.rel_int[indice];
source_respaldo.change.emit();
source.change.emit();
console.log("callback completed");