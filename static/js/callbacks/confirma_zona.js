var progreIni = 'pk' + text_input_prog_ini.value;
var progreFin = 'pk' + text_input_prog_fin.value;
var s_data = source.data;
var s_data_respaldo = source_respaldo.data;
var s_data_cuadrados = source_cuadrados.data;
var rel_int_ant = 0
function range(start, end) {
    var ans = [];
    for (let i = start; i <= end; i++) {
        ans.push(i);
    }
    return ans;
} 
var i = 0;
var k = 0;
var ultimo = s_data.Eventos_permitidos.length;
var largoFinal = s_data.RT.length + 2;
if (!(s_data.ProgresivaFin.includes(progreFin + '.00')) && !(s_data.ProgresivaIni.includes(progreIni + '.00'))){
    for (var m = 0; m < ultimo; m++){
        console.log(s_data.ProgresivaFin[m].split('pk')[1])
        if ((parseInt(s_data.ProgresivaFin[m].split('pk')[1]) < parseInt(progreFin.split('pk')[1])) && (parseInt(s_data.ProgresivaFin[m].split('pk')[1]) > parseInt(progreIni.split('pk')[1]))){
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
            ultimo--;
            break;
        }
    }
    while(k < 2){
        console.log(i)
        if (k === 0){
            if ((parseInt(s_data.ProgresivaFin[i].split('pk')[1]) > parseInt(progreFin.split('pk')[1]))){
                for (var j = ultimo; j > i; j--){
                    console.log(j)
                    s_data.RT[j] = s_data.RT[j - 1];
                    s_data.RT_intensity[j] = s_data.RT_intensity[j - 1];
                    s_data.Eventos_permitidos[j] = s_data.Eventos_permitidos[j - 1];
                    s_data.index[j] = s_data.index[j - 1] + 1;
                    s_data.color[j] = s_data.color[j - 1];
                    s_data.Intensity_tip[j] = 'Zona ' + (j).toString();
                    s_data.rel_int = [].slice.call(s_data.rel_int);
                    s_data.rel_int[j] = s_data.rel_int[j - 1];
                    s_data.ProgresivaIni[j] = s_data.ProgresivaIni[j - 1];
                    s_data.ProgresivaFin[j] = s_data.ProgresivaFin[j - 1];
                    s_data_cuadrados.x[j] = s_data_cuadrados.x[j - 1];
                    s_data_cuadrados.y[j] = s_data_cuadrados.y[j - 1];
                    s_data_cuadrados.color[j] = s_data_cuadrados.color[j - 1];
                    s_data_cuadrados.index[j] = s_data_cuadrados.index[j - 1] + 1;
                    s_data_cuadrados.cont[j] = s_data_cuadrados.cont[j - 1];
                }
                if (i == 0){
                    var valorFin = (parseInt(progreFin.split('pk')[1]) - 338) * 1000 + 510;
                    var valorIni = (338 - 338) * 1000 + 510;
                }
                else{
                    var valorFin = (parseInt(progreFin.split('pk')[1]) - 338) * 1000 + 510;
                    var valorIni = (parseInt(s_data.Intensity_tip[i - 1].split('pk')) - 338) * 1000 + 510;
                }
                s_data.RT[i] = new Array(50);
                s_data.RT[i].fill(valorFin);
                s_data.RT_intensity[i] = range(0, 49);
                s_data.Eventos_permitidos[i] = 'Camioneta/Retroexcavadora/Camion';
                s_data.index[i] = i;
                s_data.color[i] = 'Orange';
                s_data.Intensity_tip[i] = 'Zona ' + i.toString();
                s_data.rel_int[i] = Math.random(0, 1);
                s_data.ProgresivaIni[i] = 'pk' + ((valorIni - 510)/1000 + 338).toString();
                s_data.ProgresivaFin[i] = 'pk' + ((valorFin - 510)/1000 + 338).toString();
                s_data_cuadrados.x[i][0][0][0] = 0;
                s_data_cuadrados.x[i][0][0][1] = 0;
                s_data_cuadrados.x[i][0][0][2] = 0;
                s_data_cuadrados.x[i][0][0][3] = 0;
                s_data_cuadrados.y[i][0][0][0] = 0;
                s_data_cuadrados.y[i][0][0][1] = 50;
                s_data_cuadrados.y[i][0][0][2] = 50;
                s_data_cuadrados.y[i][0][0][3] = 0;
                s_data_cuadrados.color[i] = 'Gray';
                s_data_cuadrados.index[i] = i;
                s_data_cuadrados.cont[i] = s_data_cuadrados.cont[ultimo];
                i = -1;
                k++;
                ultimo++;
            }
        }
        
        else if (k === 1){
            if ((parseInt(s_data.ProgresivaFin[i].split('pk')[1]) > parseInt(progreIni.split('pk')[1]))){
                for (var j = ultimo; j > i; j--){
                    console.log(j)
                    s_data.RT[j] = s_data.RT[j - 1];
                    s_data.RT_intensity[j] = s_data.RT_intensity[j - 1];
                    s_data.Eventos_permitidos[j] = s_data.Eventos_permitidos[j - 1];
                    s_data.index[j] = s_data.index[j - 1] + 1;
                    s_data.color[j] = s_data.color[j - 1];
                    s_data.Intensity_tip[j] = 'Zona ' + (j).toString();
                    s_data.rel_int = [].slice.call(s_data.rel_int);
                    s_data.rel_int[j] = s_data.rel_int[j - 1];
                    s_data.ProgresivaIni[j] = s_data.ProgresivaIni[j - 1];
                    s_data.ProgresivaFin[j] = s_data.ProgresivaFin[j - 1];
                    s_data_cuadrados.x[j] = s_data_cuadrados.x[j - 1];
                    s_data_cuadrados.y[j] = s_data_cuadrados.y[j - 1];
                    s_data_cuadrados.color[j] = s_data_cuadrados.color[j - 1];
                    s_data_cuadrados.index[j] = s_data_cuadrados.index[j - 1] + 1;
                    s_data_cuadrados.cont[j] = s_data_cuadrados.cont[j - 1];
                }
                if (i === 0){
                    var valorFin = (parseInt(progreIni.split('pk')[1]) - 338) * 1000 + 510;
                    var valorIni = (338 - 338) * 1000 + 510;;
                }
                else{
                    var valorFin = (parseInt(progreIni.split('pk')[1]) - 338) * 1000 + 510;
                    var valorIni = (parseInt(s_data.Intensity_tip[i - 1].split('pk')) - 338) * 1000 + 510;
                }
                s_data.RT[i] = new Array(50);
                s_data.RT[i].fill(valorFin);
                s_data.RT_intensity[i] = range(0, 49);
                s_data.Eventos_permitidos[i] = 'Camioneta/Retroexcavadora/Camion';
                s_data.index[i] = i;
                s_data.color[i] = 'Orange';
                s_data.Intensity_tip[i] = 'Zona ' + i.toString();
                s_data.rel_int[i] = Math.random(0, 1);
                s_data.ProgresivaIni[i] = 'pk' + ((valorIni - 510)/1000 + 338).toString();
                s_data.ProgresivaFin[i] = 'pk' + ((valorFin - 510)/1000 + 338).toString();
                s_data_cuadrados.x[i][0][0][0] = 0;
                s_data_cuadrados.x[i][0][0][1] = 0;
                s_data_cuadrados.x[i][0][0][2] = 0;
                s_data_cuadrados.x[i][0][0][3] = 0;
                s_data_cuadrados.y[i][0][0][0] = 0;
                s_data_cuadrados.y[i][0][0][1] = 50;
                s_data_cuadrados.y[i][0][0][2] = 50;
                s_data_cuadrados.y[i][0][0][3] = 0;
                s_data_cuadrados.color[i] = 'Gray';
                s_data_cuadrados.index[i] = i;
                s_data_cuadrados.cont[i] = 0;
                i = -1;
                k++;
                ultimo++;
            }
        }
        i++;
    }
    var largoActual = s_data.RT.length;
    var largo = s_data.RT.length;
    for (var i = 0; i < largo; i++){
        if (i !== 0){
            s_data_cuadrados.x[i] = [[[s_data.RT[i - 1][0], s_data.RT[i - 1][0], s_data.RT[i][0], s_data.RT[i][0]]]];
        }
        else{
            s_data_cuadrados.x[i] = [[[0, 0, s_data.RT[i][0], s_data.RT[i][0]]]];
        }
        console.log(s_data_cuadrados.x[i][0][0])
        if (i === 0){
            s_data.ProgresivaIni[i] = 'pk338';
        }
        else{
            s_data.ProgresivaIni[i] = s_data.ProgresivaFin[i - 1];
        }
        var suma = (s_data.RT[i][0] - 510)/1000 + 338;
        s_data.ProgresivaFin[i] = 'pk' + ((suma.toFixed(2).toString()));
    }
    source_cuadrados.change.emit();
    select.options = s_data.Intensity_tip;
    source.change.emit();
}