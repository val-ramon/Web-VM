var s_data = source.data;        
for (var m = 0; m < source.data.RT.length; m++){
    if (s_data.Intensity_tip[m] === select.value){
        s_data.RT.splice(m, 1);
        s_data.RT_intensity.splice(m, 1);
        s_data.Eventos_permitidos.splice(m, 1);
        s_data.index.splice(m, 1);
        s_data.color.splice(m, 1);
        s_data.Intensity_tip.splice(m, 1);
        s_data.rel_int = [].slice.call(s_data.rel_int);
        s_data.rel_int.splice(m, 1);
        s_data.ProgresivaIni.splice(m, 1);
        s_data.ProgresivaFin.splice(m, 1);
        s_data_cuadrados.x.splice(m, 1);
        s_data_cuadrados.y.splice(m, 1);
        s_data_cuadrados.color.splice(m, 1);
        s_data_cuadrados.index.splice(m, 1);
        s_data_cuadrados.cont.splice(m, 1);
        break;
    }
}
var largo = s_data.RT.length;
    for (var i = 0; i < largo; i++){
        if (i !== 0){
            s_data_cuadrados.x[i] = [[[s_data.RT[i - 1][0], s_data.RT[i - 1][0], s_data.RT[i][0], s_data.RT[i][0]]]];
        }
        else{
            s_data_cuadrados.x[i] = [[[0, 0, s_data.RT[i][0], s_data.RT[i][0]]]];
        }
        if (i === 0){
            s_data.ProgresivaIni[i] = 'pk338';
        }
        else{
            s_data.ProgresivaIni[i] = s_data.ProgresivaFin[i - 1];
        }
        var suma = (s_data.RT[i][0] - 510)/1000 + 338;
        s_data.ProgresivaFin[i] = 'pk' + ((suma.toFixed(2).toString()));
    }
source.change.emit();