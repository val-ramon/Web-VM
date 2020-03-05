// Los sources y la tabla vienen como parametros desde Python mediante la funcion CustomJS, donde se pasan los parametros como diccionarios

var value_slider = cb_obj['value']; // Toma los valores del range slider y los asigna a una variable, esto viene como tupla.
source_filtros.data.rango_pk[0] = cb_obj['value']; // Le asigna al source de filtros los valores del slider para poder usarlos en otros filtros.

var fechaIni;
var fechaFin;
var fechaI;
var fechaF;
// Toma las fechas del source de filtros, la separa por barras y las transforma en formato Date para poder realizar operaciones
if (source_filtros.data.rango_fecha[0][0].includes('/')){
	fechaI = source_filtros.data.rango_fecha[0][0].split('/');
}
else {
	fechaI = source_filtros.data.rango_fecha[0][0].split('-');
}
if (source_filtros.data.rango_fecha[0][1].includes('/')){
	fechaF = source_filtros.data.rango_fecha[0][1].split('/');
}
else {
	fechaF = source_filtros.data.rango_fecha[0][1].split('-');
}

fechaIni = new Date(fechaI[0], fechaI[1], fechaI[2]);
fechaFin = new Date(fechaF[0], fechaF[1], fechaF[2]);

data_table.visible = false; // Hace invisible la tabla por un momento para simular actualizacion en tiempo real

var j = 0;

// Vacias los vectores del source donde se van a colocar los datos filtrados para que no haya conflictos al sobreescribir
source_historicos_filtrado.data.id = [];
source_historicos_filtrado.data.progre = [];
source_historicos_filtrado.data.fecha = [];
source_historicos_filtrado.data.vehi = [];
source_historicos_filtrado.data.estado = [];

/* Recorre todo el source de la base de datos buscando coincidencias entre valores, en caso de que se de dicha coincidencia, se va agregando
    al source que se usa para mostrar los datos filtrados*/
var fechaCompara;
for (var i = 0; i < source_historicos.data.progre.length; i++){
    fechaCompara = source_historicos.data.fecha[i].split(',')[0].split('/');
    if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && source_filtros.data.vehiculo[0].includes(source_historicos.data.vehi[i]) && source_filtros.data.estado[0].includes(source_historicos.data.estado[i]) && (new Date(fechaCompara[0], fechaCompara[1], fechaCompara[2]) <= fechaFin && new Date(fechaCompara[0], fechaCompara[1], fechaCompara[2]) >= fechaIni)){
        source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
        source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
        source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
        source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
        source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
        j++;
    }
}

// Al terminar esto, se le asigna la nueva data a la tabla y se la vuelve a mostrar nuevamente
data_table.source = source_historicos_filtrado;
data_table.visible = true;
