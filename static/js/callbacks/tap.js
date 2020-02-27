// Los datos de los sources, el select, el slider, el checkbox de eventos, los botones y las herramientas llegan por parametros desde Python

var s_data = source.data; // Guarda la data del source de zonas en una variable
var x = cb_obj['x']; // Como esta funcion detecta los clicks en la figura, se fija la coordenada en x para saber donde se hizo click
var eve = []; // Crea un vector para poder agregar los eventos permitidos de la zona seleccionada 
var s_data_cuadrados = source_cuadrados.data; // Guarda en una variable los datos del source de sombreado de zonas

/* Primero se fija si la herramienta para modificar zonas esta activa, si no lo esta, la activa y se fija en que zona se hizo click,
    esto es para darle al usuario una nocion visual de que zona esta modificando*/
if (draw_tool_l1.active === false) {
    draw_tool_l1.active = true; // Activa herramienta de modificacion de zonas
    for (var i = 0; i < s_data_cuadrados.color.length; i++){
        if (s_data.Eventos_permitidos[i].includes('Ninguno')){
            s_data_cuadrados.color[i] = 'White';
        }
        else{
            s_data_cuadrados.color[i] = 'Grey';
        }
    }

    /* Recorre todo el source de las zonas para verificar que la coordenada en x coincida con alguna zona, una vez que la encuentra, la marca
        y permite modificar la zona, mostrando la zona seleccionada con un color distinto, a su vez que modifica el select, lo bloquea y 
        cambia la intensidad relativa y eventos permitidos a los de la zona*/
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
    boton_muestra_eventos_zona.disabled = false; // Habilita el boton de mostrar ultimos eventos de zona
    boton_elimina_zona.disabled = false; // Habilita el boton para eliminar zona, ya que hay una seleccionada
}
else{
    /* En caso de que haya zonas seleccionadas y se vuelva a hacer click, deshabilita todos los botones y la tabla de ultimos eventos
        asi como la herramienta para modificar zonas */
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

// Emite todos los cambios correspondientes en los sources
source_respaldo.data = source.data;
source_respaldo.change.emit();
source.change.emit();
source3.change.emit();
source_cuadrados.change.emit();
