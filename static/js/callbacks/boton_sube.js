// La tabla y los sources que contienen los datos de la base de datos llegan desde Python como parametros

data_table.visible = false; // Oculta la tabla momentaneamente para simular actualizacion en tiempo real y mostrar nuevos datos
sourceIteraHistoricos.data.cont[0]++;
botonBaja.visible = true; // Activa el boton para visualizar menos eventos una vez que se cargan los mismos en la tabla
cb_obj['label'] = 'Cargar mas eventos';

/* Se fija los valores alto y bajo para saber desde donde tomar los nuevos eventos, agregando de a 500 eventos historicos*/
var masBajo = (sourceIteraHistoricos.data.cont[0]) * 500;
var masAlto = (sourceIteraHistoricos.data.cont[0] + 1) * 500;

// Comprueba que los valores no sobrepasen el largo total de la base de datos, en caso contrario, los modifica

// Luego mediante el bucle for los va agregando para luego mostrarlos
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

// Modifica el source de la tabla y la hace nuevamente visible para visualizar los cambios
data_table.source = source_historicos;
data_table.visible = true;
