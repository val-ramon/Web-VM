// La tabla y los sources que contienen los datos de la base de datos llegan desde Python como parametros

data_table.visible = false; // Oculta la tabla momentaneamente para simular actualizacion en tiempo real y mostrar nuevos datos
sourceIteraHistoricos.data.cont[0]++; // Suma el contador para saber donde esta parado en cantidad de eventos
botonBaja.visible = true; // Activa el boton para visualizar menos eventos una vez que se cargan los mismos en la tabla
cb_obj['label'] = 'Cargar mas eventos';
// La tabla y los sources que contienen los datos de la base de datos llegan desde Python como parametros

data_table.visible = false; // Oculta la tabla momentaneamente para simular actualizacion en tiempo real y mostrar nuevos datos
sourceIteraHistoricos.data.cont[0]++; // Suma el contador para saber donde esta parado en cantidad de eventos
botonBaja.visible = true; // Activa el boton para visualizar menos eventos una vez que se cargan los mismos en la tabla
cb_obj['label'] = 'Cargar mas eventos';

/* Se fija los valores alto y bajo para saber desde donde tomar los nuevos eventos, agregando de a 500 eventos historicos*/
var largo = (sourceIteraHistoricos.data.cont[0]) * 500;
var masAlto = source_todos_historicos.data.progre.length;
var masBajo = masAlto - largo;
var j = 0

// Comprueba que los valores no sobrepasen el largo total de la base de datos, en caso contrario, los modifica

// Luego mediante el bucle for los va agregando para luego mostrarlos
if (masBajo < 0){
    masBajo = 0;
    cb_obj.disabled = true;
}
for (var i = masBajo; i < masAlto; i++) {
    source_historicos.data.id[j] = source_todos_historicos.data.id[i];
    source_historicos.data.progre[j] = source_todos_historicos.data.progre[i];
    source_historicos.data.fecha[j] = source_todos_historicos.data.fecha[i];
    source_historicos.data.vehi[j] = source_todos_historicos.data.vehi[i];
    source_historicos.data.estado[j] = source_todos_historicos.data.estado[i];
    j++;
}
// Modifica el source de la tabla y la hace nuevamente visible para visualizar los cambios
data_table.source = source_historicos;
data_table.visible = true;
