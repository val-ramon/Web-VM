var s_data = source.data;
var x = cb_obj['x'];
var eve = [];
s_data_cuadrados = source_cuadrados.data;
if (draw_tool_l1.active === false) {
    draw_tool_l1.active = true;
    for (var i = 0; i < s_data_cuadrados.color.length; i++){
        if (s_data.Eventos_permitidos[i].includes('Ninguno')){
            s_data_cuadrados.color[i] = 'White';
        }
        else{
            s_data_cuadrados.color[i] = 'Grey';
        }
    }
    var encontrado = false;
    for (var i = 0; i < s_data.RT.length; i++){
        if (i !== 0){
            if ((x < s_data.RT[i][0]) && (x > s_data.RT[i-1][0])) {
                select.value = s_data.Intensity_tip[i];
                select.disabled = true;
                source3.data.zona[0] = s_data.Intensity_tip[i];
                for (var k = 0; k < eventos_perm.length; k++){
                    if (s_data.Eventos_permitidos[i].includes(eventos_perm[k])){
                        eve.push(k);
                    }
                }
                eventos.active = eve;
                slider.value = s_data.rel_int[i];
                
                s_data_cuadrados.color[i] = 'Red';
                encontrado = true;
            }
            if (encontrado === false){
                if (s_data.Eventos_permitidos[i].includes('Ninguno')){
                    s_data_cuadrados.color[i] = 'White';
                }
                else{
                    s_data_cuadrados.color[i] = 'Grey';
                }
                select.disabled = false;
            }
        }
        else{
            if ((x < s_data.RT[i][0]) && (x > 0)) {
                select.value = s_data.Intensity_tip[i];
                select.disabled = true;
                source3.data.zona[0] = s_data.Intensity_tip[i];
                for (var k = 0; k < eventos_perm.length; k++){
                    if (s_data.Eventos_permitidos[i].includes(eventos_perm[k])){
                        eve.push(k);
                    }
                }
                eventos.active = eve;
                slider.value = s_data.rel_int[i];
                
                s_data_cuadrados.color[i] = 'Red';
                encontrado = true;
                
            }
            if (encontrado === false){
                if (s_data.Eventos_permitidos[i].includes('Ninguno')){
                    s_data_cuadrados.color[i] = 'White';
                }
                else{
                    s_data_cuadrados.color[i] = 'Grey';
                }
                select.disabled = false;
            }
        }
    }
    boton_muestra_eventos_zona.disabled = false;
    boton_elimina_zona.disabled = false;
}
else{
    boton_elimina_zona.disabled = true;
    boton_muestra_eventos_zona.disabled = true;
    div2.visible = false;
    boton_muestra_eventos_zona.label = 'Mostrar ultimos eventos de zona';
    data_table.visible = false;
    draw_tool_l1.active = false;
    for (var i = 0; i < s_data_cuadrados.color.length; i++){
        if (s_data.Eventos_permitidos[i].includes('Ninguno')){
            s_data_cuadrados.color[i] = 'White';
        }
        else{
            s_data_cuadrados.color[i] = 'Grey';
        }
    }
    select.disabled = false;
}
source_respaldo.data = source.data;
source_respaldo.change.emit();
source.change.emit();
source3.change.emit();
source_cuadrados.change.emit();