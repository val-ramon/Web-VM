var s_data_cuadrados = source_cuadrados.data;
var s_data = source.data;
s_data.RT[s_data.RT.length - 1].fill(largo_ducto);
for (var i = 0; i < s_data_cuadrados.color.length; i++){
    if (s_data.Eventos_permitidos[i].includes('Ninguno')){
        s_data_cuadrados.color[i] = 'White';
    }
    else{
        s_data_cuadrados.color[i] = 'Grey';
    }
}
source_respaldo.data = source.data;
s_data_cuadrados.cont[0] = 0;
draw_tool_l1.active = false;
boton_elimina_zona.disabled = true;
source_cuadrados.change.emit();