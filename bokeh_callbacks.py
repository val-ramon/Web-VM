# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:42:57 2020

@author: valramon
"""

from bokeh.models import  CustomJS
#Callbacks writed in JS for the logic on the website
    
def checkbox(source, source2_respaldo, source_respaldo, oculta_zonas): 
    """
        Esta funcion recibe como parametros el source original y uno de respaldo para poder recordar
        las posiciones en x, luego lo que hace es llenar todas las posiciones en x en NaN's. En caso de lo que se haga
        sea mostrar las zonas, rellena con los antiguos valores en x mediante el source de respaldo.
    """
    callback_checkbox = CustomJS(args = {'source': source, 'source2': source2_respaldo, 'source_respaldo': source_respaldo, 'labs' : oculta_zonas},
        code = """
        var s_data = source.data;
        var s_data_respaldo = source2.data;
        var select_vals = cb_obj.active.map(function(x){return cb_obj.labels[x];});
        var nan = NaN;
        for (var i = 0; i < s_data_respaldo.x.length; i++){
            if(!isNaN(s_data.RT[i][0])){
                s_data_respaldo.x[i].fill(s_data.RT[i][0]);
            }
        }
        const y_old = y;
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
        source_respaldo = source;
        source.change.emit();
        console.log("callback completed");
        """)
    return callback_checkbox

def guarda_zona(source3):
    """
        Este callback sirve solamente para el select, el cual ayuda a 'recordar' la zona que se modifica.
    """
    guarda_zona = CustomJS(args = {'source3': source3}, 
        code = """
        var f = cb_obj.value;
        zona = source3.data.zona;
        zona[0] = f;
        source3.change.emit();
        console.log("callback completed");
        """)
    return guarda_zona

def evento(source, source3, source_respaldo, source_cuadrados):
    """
        En esta funcion se recorre el checkbox de los eventos para determinar cuales son los activos, y en base a eso
        modifica el source original para poder asignar los nuevos eventos permitidos en la zona a modificar.
        Se le asigna un color (naranja) si la zona permite eventos, si no los permite, se le asigna otro color (gris)
        simbolizando la zona silenciada.
    """
    callback_evento = CustomJS(args = {'source': source, 'source3' : source3, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados},
        code = """
        var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];});
        var nueva_data = source3.data;
        var indice = source.data.Intensity_tip.indexOf(nueva_data.zona[0]);
        if (data.includes("Ninguno") && data.length === 1){
            source.data.color[indice] = "Gray";
            source_cuadrados.data.color[indice] = 'White';
        }
        if (data.length === 1 && !data.includes("Ninguno")){
            source.data.color[indice] = "Orange";
        }
        if (data.length === 2 && !data.includes("Ninguno")){
            source.data.color[indice] = "Orange";
        }
        if (data.length === 3 && !data.includes("Ninguno")){
            source.data.color[indice] = "Orange";
        }
        source.data.Eventos_permitidos[indice] = (data.toString()).replace(/,/g, "/");
        source.change.emit();
        console.log("callback completed");
        """)
    return callback_evento

def intensidad(source, source3, source_respaldo):
    """
        Mediante esta funcion se toma el valor actual del slider cada vez que se lo modifica para así ir modificando
        en tiempo real la intensidad relativa de la zona a modificar.
    """
    callback_int = CustomJS(args = {'source': source, 'source3' : source3, 'source_respaldo': source_respaldo},
        code = """
        var s_data = source.data;
        var data = cb_obj.value;
        var nueva_data = source3.data;
        var indice = s_data.Intensity_tip.indexOf(nueva_data.zona[0]);

        s_data.rel_int[indice] = data.toFixed(2);
        source.change.emit();
        console.log("callback completed");
        """)
    return callback_int

def deshace_cambios(source, source_respaldo, source_cuadrados, input_eventos, slider_intensidad, eventos_perm, source3, poly_draw_tool):
    """
                FUNCION TODAVÍA EN REVISIÓN
                
        Esta funcion como propósito tiene el poder volver al último cambio realizado, tanto en movimiento de zonas como
        en cambio de eventos permitidos e intensidad relativa.
        
            Por el momento lo que hace es volver a la intensidad
        relativa anterior y a los últimos eventos modificados, y elimina líneas creadas a partir de la herramienta
        que permite mover zonas. Falta agregar que pueda volver la última zona modificada
        a su posición anterior.
    """
    
    callback_deshace_cambios = CustomJS(args = {'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados,
                                                'eventos_perm': eventos_perm, 'eventos':input_eventos, 'slider': slider_intensidad, 'source3' : source3, 'poly_draw_tool': poly_draw_tool},
        code = """
        var s_data_cuadrados = source_cuadrados.data;
        var eve = [];
        s_data_respaldo = source_respaldo.data;
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
        """)
        
    return callback_deshace_cambios
    
def download(source):
    """
        Recibe como parámetro el source que contiene todos los datos de las zonas, lo transforma en un string largo,
        el cual se forma concatenando cada fila con un salto de línea y cada columna con una coma.
        Esto generada un archivo '.csv' en el navegador que se descarga desde el mismo.
        En la próxima carga de la página principal del mapa, este archivo sirve como nuevos parámetros para el mapa.
    """
    callback_download = CustomJS(args={'source': source},
        code = """
        function table_to_csv(source) {
            var columns = Object.keys(source.data);
            const nrows = source.get_length();
            var lugar = columns.indexOf("RT_intensity");
            columns.splice(lugar, 1);
            lugar = columns.indexOf("index");
            columns.splice(lugar, 1);
            var lines = [columns.join(',')];
            for (let i = 0; i < nrows; i++) {
                let row = [];
                for (let j = 0; j < columns.length; j++) {
                    const column = columns[j];
                    if (column !== "RT_intensity"){
                        if (column !== "ProgresivaFin" && column !== "ProgresivaIni" && column !== "RT"){
                            row.push((source.data[column][i].toString()).replace(/,/g, "/"));
                        }
                        else if (column === "RT"){
                            row.push(source.data[column][i][0].toString());
                        }
                        else{
                            row.push(source.data[column][i].toString());
                        }
                    }
                }
                lines.push(row.join(','));
            }
            return lines.join('\\n').concat('\\n');
        }
        
        const filename = 'change_emmited.csv';
        filetext = table_to_csv(source);
        filetext = filetext.slice(0, filetext.length - 1);
        const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });
        
        //addresses IE
        if (navigator.msSaveBlob) {
            navigator.msSaveBlob(blob, filename);
        } else {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.target = '_blank';
            link.style.visibility = 'hidden';
            link.dispatchEvent(new MouseEvent('click'));
        }

        console.log("callback completed");
        """)
    return callback_download

def mouse_drag(source, source_cuadrados, source3, select, poli, slider_intensidad, input_eventos, eventos_perm, source_respaldo, largo_ducto):
    """
        En esta función se detectan los cambios en x de cada zona y las va modificando en tiempo real, evitando que
        quede alguna zona colgada.
        Toma todos los datos del source original y del source del sombreado de las zonas y los va comparando sobre la
        modificación en tiempo real para que vayan a la par.
        A su vez modifica la progresiva en base a la posición en x de cada zona.
        También muestra la zona que se está seleccionando y modificando en ese momento.
    """
    
    callback_mouse = CustomJS(args={'source': source, 'source_cuadrados':source_cuadrados, 'source3': source3, 'select': select, 'poli': poli,
                                    'slider': slider_intensidad, 'eventos': input_eventos, 'eventos_perm': eventos_perm, 'source_respaldo': source_respaldo, 'largo_ducto': largo_ducto}, 
            code="""
            var s_data = source.data;
            var s_data_cuadrados = source_cuadrados.data;
            var largo = s_data_cuadrados.x.length;
            var modifica = '';
            var eve = [];
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
                if (i === 0){
                    s_data.ProgresivaIni[i] = 'pk338';
                }
                else{
                    s_data.ProgresivaIni[i] = s_data.ProgresivaFin[i - 1];
                }
                var suma = (s_data.RT[i][0] - 510)/1000 + 338;
                s_data.ProgresivaFin[i] = 'pk' + ((suma.toFixed(2).toString()));
            }
            s_data.RT[largo - 1].fill(largo_ducto);
            source3.change.emit();
            source.change.emit();
            source_cuadrados.change.emit();
        """)
    return callback_mouse

def mouse_end(poli, source_cuadrados, source, largo_ducto, draw_tool_l1, boton_elimina_zona, source_respaldo):
    """
        Esta función lo único que hace es detectar cuando el mouse deja de estar realizando cambios sobre la figura
        y deja de mostrar la zona activa, además de que desactiva la herramienta que sirve para modificar las zonas.
    """
    
    callback_mouse_end = CustomJS(args={'poli': poli, 'source_cuadrados': source_cuadrados, 'source': source, 'largo_ducto': largo_ducto, 'draw_tool_l1': draw_tool_l1, 'boton_elimina_zona': boton_elimina_zona, 'source_respaldo': source_respaldo}, code="""                    
            s_data_cuadrados = source_cuadrados.data;
            s_data = source.data;
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
        """)
    return callback_mouse_end

def mouse_move(source, source_respaldo, source_cuadrados):
    """
        Esta función se creó con el fin de que por más que se quisiese mover una zona fuera de la figura, siempre
        mantenga sus coordenadas en y.
    """
    callback_mouse_move = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados':source_cuadrados}, code="""
            function range(start, end) {
                var ans = [];
                for (let i = start; i <= end; i++) {
                    ans.push(i);
                }
                return ans;
            } 
            for (var j = 0; j < source.data.RT.length; j++){
                source.data.RT_intensity[j] = range(0, 49);
            }
            source.change.emit();
        """)
    return callback_mouse_move

def mouse_guarda(source, source_respaldo, source_cuadrados):
    """
        Función con el fin de poder guardar los datos de la antigua posición en x de cada zona para poder deshacer
        cambios. 
            NO FUNCIONA CORRECTAMENTE.
    """
    callback_mouse_guarda = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados':source_cuadrados}, code="""
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
        """)
    return callback_mouse_guarda

def tap(source, source_respaldo, source3, source_cuadrados, slider_intensidad, input_eventos, eventos_perm, select, poli, draw_tool_l1, boton_elimina_zona, boton_muestra_eventos_zona, data_table, div2):
    """
        Detecta el click sobre la figura, determina las coordenadas en x correspondientes a la zona, actualiza el
        select de la zona automáticamente y los deshabilita mientras haya una zona seleccionada.
        
        Esta función habilita automáticamente la herramienta para modificar zonas.
    """
    
    callback_tap = CustomJS(args={'source': source, 'source3': source3,'source_cuadrados':source_cuadrados,'slider': slider_intensidad, 'eventos': input_eventos, 'eventos_perm': eventos_perm, 'select': select, 'poli': poli, 'draw_tool_l1': draw_tool_l1, 'boton_elimina_zona': boton_elimina_zona, 'source_respaldo': source_respaldo, 'boton_muestra_eventos_zona': boton_muestra_eventos_zona, 'data_table': data_table, 'div2': div2}, code="""
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
        """)
    return callback_tap

def muestra_eventos_zona(source, source_eventos, source_historicos_muestra, data_table, select, div2):
    """
        En esta función, siempre y cuando haya una zona seleccionada previamente, lo que se hace es mostrar los
        últimos 10 eventos correspondientes a las progresivas comprendidas en la zona seleccionada.
    """
    callback_muestra_eventos_zona = CustomJS(args={'source': source, 'source_eventos': source_eventos, 'source_historicos_muestra': source_historicos_muestra, 'dataTable': data_table, 'select': select, 'div2': div2}, code="""
            var label = cb_obj['label'];
            var nueva_data = select.value;
            var indice = source.data.Intensity_tip.indexOf(nueva_data);
            var j = 9;
            var data_source_historicos_muestra = source_historicos_muestra.data;
            data_source_historicos_muestra.progre = [];
            data_source_historicos_muestra.id = [];
            data_source_historicos_muestra.vehi = [];
            data_source_historicos_muestra.fecha = [];
            data_source_historicos_muestra.estado = [];
            if (label === 'Mostrar ultimos eventos de zona'){
                for (var i = source_eventos.data.progre.length - 1; i >= 0; i--){
                    if (parseInt(source_eventos.data.progre[i]) >= parseInt(source.data.ProgresivaIni[indice].split('pk')[1]) && (source_eventos.data.progre[i] <= parseInt(source.data.ProgresivaFin[indice].split('pk')[1])) && j >= 0){
                        data_source_historicos_muestra.progre[j] = source_eventos.data.progre[i];
                        data_source_historicos_muestra.id[j] = source_eventos.data.id[i];
                        data_source_historicos_muestra.vehi[j] = source_eventos.data.vehi[i];
                        data_source_historicos_muestra.fecha[j] = source_eventos.data.fecha[i];
                        data_source_historicos_muestra.estado[j] = source_eventos.data.estado[i];
                        j--;
                    }
                }
                source_historicos_muestra.change.emit();
                dataTable.source = source_historicos_muestra;
                dataTable.visible = true;
                div2.visible = true;
                cb_obj['label'] = 'Ocultar ultimos eventos de zona';
            }
            else{
                dataTable.visible = false;
                div2.visible = false;
                cb_obj['label'] = 'Mostrar ultimos eventos de zona';
            }
        """)
    return callback_muestra_eventos_zona

def muestra_todos_eventos(source_cambia_paginas):
    """
        NO USADA/NO FUNCIONA CORRECTAMENTE.
        
        Función creada para alternar entre mapa e históricos, pero se reemplazó por otro método.
    """
    callback_muestra_eventos_zona = CustomJS(args={'source_cambia_paginas': source_cambia_paginas}, code="""
            source_cambia_paginas.data.pagina[0] = 1;
        """)
    return callback_muestra_eventos_zona

def agrega_zona(text_input_prog_ini, text_input_prog_fin, boton_confirma_zona):
    """
        NO USADA ACTUALMENTE.
        
        Esta función alterna entre labels de un botón que sirve para agregar zonas, el cual habilita dicha herramienta.
    """
    
    callback_agrega_zona = CustomJS(args={'text_input_prog_ini': text_input_prog_ini, 'text_input_prog_fin': text_input_prog_fin, 'boton_confirma_zona': boton_confirma_zona}, code="""
            if (cb_obj.label === 'Agregar zonas'){
                cb_obj.label = 'Terminar de agregar zonas';
                text_input_prog_ini.visible = true;
                text_input_prog_fin.visible = true;
                boton_confirma_zona.visible = true;
            }
            else{
                cb_obj.label = 'Agregar zonas';
                text_input_prog_ini.visible = false;
                text_input_prog_fin.visible = false;
                boton_confirma_zona.visible = false;
            }
        """)
    return callback_agrega_zona

def confirma_zona(source, source_respaldo, source_cuadrados, select, text_input_prog_ini, text_input_prog_fin):
    """
        Toma las progresivas inicial y final donde se agregará la nueva zona. Cabe destacar que por cada división
        de zona que se escriba (inicial, final) se generan tres zonas.
        Además verifica si hay alguna zona existente ya entre las progresivas que se ingresan, en caso de existir,
        la elimina para agregar la nueva zona.
    """
    
    callback_agrega_zona = CustomJS(args={'source': source, 'source_respaldo': source_respaldo, 'source_cuadrados': source_cuadrados, 'select': select,'text_input_prog_ini': text_input_prog_ini, 'text_input_prog_fin': text_input_prog_fin}, code="""
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
        """)
    return callback_agrega_zona

def elimina_zona(source, select):
    """
        Esta es una función que lo que hace es, si hay una zona seleccionada, permite eliminarla en caso de que ya
        no sea necesaria y la elimina totalmente, tanto funcional como visualmente.
    """
    
    callback_elimina_zona = CustomJS(args={'source': source, 'select': select}, code="""
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
        """)
    return callback_elimina_zona




def filtra_rango_pk(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es tomar los rangos de progresiva a filtrar y muestra solamente los eventos comprendidos en ese
        rango de progresivas. A su vez, las filtra en base a los demás filtros (fecha, estado, vehiculo).
    """    
    
    callback_filtra_rango_pk = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros}, code="""
            var value_slider = cb_obj['value'];
            source_filtros.data.rango_pk[0] = cb_obj['value']; 
            var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
            var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));
            data_table.visible = false;
            var j = 0;
            source_historicos_filtrado.data.id = [];
            source_historicos_filtrado.data.progre = [];
            source_historicos_filtrado.data.fecha = [];
            source_historicos_filtrado.data.vehi = [];
            source_historicos_filtrado.data.estado = [];
            for (var i = 0; i < source_historicos.data.progre.length; i++){
                if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && source_filtros.data.vehiculo[0].includes(source_historicos.data.vehi[i]) && source_filtros.data.estado[0].includes(source_historicos.data.estado[i]) && (new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) <= fechaFin && new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) >= fechaIni)){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
            }
            data_table.source = source_historicos_filtrado;
            data_table.visible = true;
        """)
    return callback_filtra_rango_pk

def filtra_vehiculos(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es mirar el checkbox y qué está seleccionado para poder filtrar en base a los vehiculos seleccionados. 
        A su vez, las filtra en base a los demás filtros (fecha, estado, progresiva).
    """    
    
    callback_filtra_vehiculos = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros}, code="""
            var value_slider = source_filtros.data.rango_pk[0];
            var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];});
            source_filtros.data.vehiculo[0] = data; 
            var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
            var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));
            data_table.visible = false;
            var j = 0;
            source_historicos_filtrado.data.id = [];
            source_historicos_filtrado.data.progre = [];
            source_historicos_filtrado.data.fecha = [];
            source_historicos_filtrado.data.vehi = [];
            source_historicos_filtrado.data.estado = [];
            for (var i = 0; i < source_historicos.data.progre.length; i++){
                if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && data.includes(source_historicos.data.vehi[i]) && source_filtros.data.estado[0].includes(source_historicos.data.estado[i]) && (new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) <= fechaFin && new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) >= fechaIni)){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
            }
            data_table.source = source_historicos_filtrado;
            data_table.visible = true;
        """)
    return callback_filtra_vehiculos

def filtra_id(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Toma el id que se ingrese en el input y busca en el source de históricos todos los eventos que tengan el mismo
        id.
    """    
    
    callback_filtra_id = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros}, code="""
            var id = cb_obj['value_input'];
            source_filtros.data.id[0] = id;
            data_table.visible = false;
            var j = 0;
            source_historicos_filtrado.data.id = [];
            source_historicos_filtrado.data.progre = [];
            source_historicos_filtrado.data.fecha = [];
            source_historicos_filtrado.data.vehi = [];
            source_historicos_filtrado.data.estado = [];
            for (var i = 0; i < source_historicos.data.progre.length; i++){
                if (source_historicos.data.id[i] === id){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
                if (id === ''){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
            }
            data_table.source = source_historicos_filtrado;
            data_table.visible = true;
        """)
    return callback_filtra_id

def filtra_estado(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Esta función sirve para la solapa de históricos.
        Lo que hace es mirar el checkbox y qué está seleccionado para poder filtrar en base a los estados seleccionados. 
        A su vez, las filtra en base a los demás filtros (fecha, vehiculo, progresiva).
    """    
    
    callback_filtra_estado = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros}, code="""
            var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];});
            var value_slider = source_filtros.data.rango_pk[0];
            source_filtros.data.estado[0] = data; 
            var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
            var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));
            data_table.visible = false;
            var j = 0;
            source_historicos_filtrado.data.id = [];
            source_historicos_filtrado.data.progre = [];
            source_historicos_filtrado.data.fecha = [];
            source_historicos_filtrado.data.vehi = [];
            source_historicos_filtrado.data.estado = [];
            for (var i = 0; i < source_historicos.data.progre.length; i++){
                if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && source_filtros.data.vehiculo[0].includes(source_historicos.data.vehi[i]) && data.includes(source_historicos.data.estado[i]) && (new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) <= fechaFin && new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) >= fechaIni)){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
            }
            data_table.source = source_historicos_filtrado;
            data_table.visible = true;
        """)
    return callback_filtra_estado

def boton_sube(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonBaja):
    """
        Esta función sirve para la solapa de históricos.
        Esta función va agregando visualmente al cuadro de históricos de a 500 eventos, inicialmente sin eventos para
        visualizar.
    """    
    
    callback_boton_sube = CustomJS(args={'source_historicos': source_historicos, 'source_todos_historicos': source_todos_historicos, 'sourceIteraHistoricos': sourceIteraHistoricos, 'data_table': data_table, 'botonBaja': botonBaja}, code="""
            data_table.visible = false;
            sourceIteraHistoricos.data.cont[0]++;
            botonBaja.visible = true;
            cb_obj['label'] = 'Cargar mas eventos'
            var masBajo = (sourceIteraHistoricos.data.cont[0]) * 500;
            var masAlto = (sourceIteraHistoricos.data.cont[0] + 1) * 500;
            if (masBajo < source_todos_historicos.data.progre.length){
                if (masAlto > source_todos_historicos.data.progre.length){
                    masAlto = source_todos_historicos.data.progre.length;
                    cb_obj.disabled = true;
                }
                for (var i = masBajo; i < masAlto; i++) {
                    source_historicos.data.id[i] = source_todos_historicos.data.id[i];
                    source_historicos.data.progre[i] = source_todos_historicos.data.progre[i];
                    source_historicos.data.fecha[i] = source_todos_historicos.data.fecha[i];
                    source_historicos.data.vehi[i] = source_todos_historicos.data.vehi[i];
                    source_historicos.data.estado[i] = source_todos_historicos.data.estado[i];
                }
            }
            else {
                cb_obj.disabled = true;
            }
            data_table.source = source_historicos;
            data_table.visible = true;
        """)
    return callback_boton_sube

def boton_baja(source_todos_historicos, source_historicos, sourceIteraHistoricos, data_table, botonSube):
    """
        Esta función sirve para la solapa de históricos.
        Esta función va quitando visualmente al cuadro de históricos de a 500 eventos, inicialmente sin eventos para
        visualizar.
    """   
    
    callback_boton_baja = CustomJS(args={'source_historicos': source_historicos, 'source_todos_historicos': source_todos_historicos, 'sourceIteraHistoricos': sourceIteraHistoricos, 'data_table': data_table, 'botonSube': botonSube}, code="""
            data_table.visible = false;
            sourceIteraHistoricos.data.cont[0]--;
            botonSube.disabled = false;
            var masBajo = (sourceIteraHistoricos.data.cont[0] + 1) * 500;
            var masAlto = (sourceIteraHistoricos.data.cont[0] + 2) * 500;
            if (masBajo <= 0){
                masbajo = 0;
                botonSube.label = 'Cargar eventos'
                cb_obj.visible = false;
            }
            for (var i = masBajo; i < masAlto; i++) {
                source_historicos.data.id[i] = [];
                source_historicos.data.progre[i] = [];
                source_historicos.data.fecha[i] = [];
                source_historicos.data.vehi[i] = [];
                source_historicos.data.estado[i] = [];
            }
            data_table.source = source_historicos;
            data_table.visible = true;
        """)
    return callback_boton_baja

def filtra_fecha_ini(source_filtros):
    """
        Toma la fecha inicial a filtrar y la guarda para poder realizar el filtrado.
    """
    
    callback_filtra_fecha_ini = CustomJS(args={'source_filtros': source_filtros}, code="""
            var fecha_ini = cb_obj['value_input'];
            source_filtros.data.rango_fecha[0][0] = fecha_ini;
        """)
    return callback_filtra_fecha_ini

def filtra_fecha_fin(source_filtros):
    """
        Toma la fecha final a filtrar y la guarda para poder realizar el filtrado.
    """
    
    callback_filtra_fecha_fin = CustomJS(args={'source_filtros': source_filtros}, code="""
            var fecha_fin = cb_obj['value_input'];
            source_filtros.data.rango_fecha[0][1] = fecha_fin;
        """)
    return callback_filtra_fecha_fin

def filtra_fecha(source_historicos, source_historicos_filtrado, data_table, source_filtros):
    """
        Toma el rango de fechas a filtrar y muestra los eventos comprendidos en ese rango de fechas.
        A su vez filtra en base a los demás parámetros de filtrado (progresiva, estado, vehiculo)
    """
    
    callback_filtra_fecha = CustomJS(args={'source_historicos': source_historicos, 'source_historicos_filtrado': source_historicos_filtrado, 'data_table': data_table, 'source_filtros': source_filtros}, code="""
            var estado = source_filtros.data.estado[0]
            var value_slider = source_filtros.data.rango_pk[0];
            var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
            var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));
            data_table.visible = false;
            var j = 0;
            source_historicos_filtrado.data.id = [];
            source_historicos_filtrado.data.progre = [];
            source_historicos_filtrado.data.fecha = [];
            source_historicos_filtrado.data.vehi = [];
            source_historicos_filtrado.data.estado = [];
            for (var i = 0; i < source_historicos.data.progre.length; i++){
                if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && source_filtros.data.vehiculo[0].includes(source_historicos.data.vehi[i]) && estado.includes(source_historicos.data.estado[i]) && (new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) <= fechaFin && new Date(source_historicos.data.fecha[i].split(',')[0].split('/')) >= fechaIni)){
                    source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
                    source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
                    source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
                    source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
                    source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
                    j++;
                }
            }
            data_table.source = source_historicos_filtrado;
            data_table.visible = true;
        """)
    return callback_filtra_fecha
