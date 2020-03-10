// La tabla y los sources que contienen los datos de la base de datos llegan desde Python como parametros

data_table.visible = false; // Oculta la tabla momentaneamente para simular actualizacion en tiempo real y mostrar nuevos datos
sourceIteraHistoricos.data.cont[0]--; // Resta el contador para saber donde esta parado en cantidad de eventos
botonSube.disabled = false; // Habilita el boton para cargar mas eventos ya que baja del tope

/* Se fija los valores alto y bajo para saber desde donde tomar los nuevos eventos, sacando de a 500 eventos historicos*/
var largo = (sourceIteraHistoricos.data.cont[0]) * 500;
var masAlto = source_todos_historicos.data.progre.length;
var masBajo = masAlto - largo;
var j = 0

// Comprueba que los valores no sobrepasen el largo total de la base de datos ni sean negativos, en caso contrario, los modifica

// Luego mediante el bucle for los va quitando para luego mostrarlos
console.log(masBajo);
console.log(largo);
if (largo <= 0){
    masbajo = 0;
    botonSube.label = 'Cargar eventos'
    cb_obj.visible = false;
	for (var i = largo; i < masAlto; i++) {
	    source_historicos.data.id[i] = [];
	    source_historicos.data.progre[i] = [];
	    source_historicos.data.fecha[i] = [];
	    source_historicos.data.vehi[i] = [];
	    source_historicos.data.estado[i] = [];
	}
}
else {
	for (var i = masBajo; i < masAlto; i++) {
	    source_historicos.data.id[j] = source_todos_historicos.data.id[i];
	    source_historicos.data.progre[j] = source_todos_historicos.data.progre[i];
	    source_historicos.data.fecha[j] = source_todos_historicos.data.fecha[i];
	    source_historicos.data.vehi[j] = source_todos_historicos.data.vehi[i];
	    source_historicos.data.estado[j] = source_todos_historicos.data.estado[i];
	    j++;
	}
}
// Modifica el source de la tabla y la hace nuevamente visible para visualizar los cambios
data_table.source = source_historicos;
data_table.visible = true;
