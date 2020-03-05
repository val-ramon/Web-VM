// Los sources y la tabla llegan desde Python pasados por parametros

var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];}); // Mapea las casillas seleccionadas en el checkbox
var value_slider = source_filtros.data.rango_pk[0]; // Toma los valores del slider de progresiva para saber donde filtrar
source_filtros.data.estado[0] = data; // Setea en el source de filtros la data de los estados utilizados para filtrar

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

data_table.visible = false; // Oculta momentaneamente la tabla para poder simular actualizacion en tiempo real de datos

/* Elimina todos los datos del source filtrado para evitar conflictos al sobreescribir con datos nuevos*/
var j = 0;
source_historicos_filtrado.data.id = [];
source_historicos_filtrado.data.progre = [];
source_historicos_filtrado.data.fecha = [];
source_historicos_filtrado.data.vehi = [];
source_historicos_filtrado.data.estado = [];

// Recorre el source de todos los datos de la base de datos para encontrar coincidencias e irlas agregando al source filtrado
var fechaCompara;
for (var i = 0; i < source_historicos.data.progre.length; i++){
    fechaCompara = source_historicos.data.fecha[i].split(',')[0].split('/');
    if (parseInt(source_historicos.data.progre[i]) >= value_slider[0] && parseInt(source_historicos.data.progre[i]) <= value_slider[1] && source_filtros.data.vehiculo[0].includes(source_historicos.data.vehi[i]) && data.includes(source_historicos.data.estado[i]) && (new Date(fechaCompara[0], fechaCompara[1], fechaCompara[2]) <= fechaFin && new Date(fechaCompara[0], fechaCompara[1], fechaCompara[2]) >= fechaIni)){
        source_historicos_filtrado.data.id[j] = source_historicos.data.id[i];
        source_historicos_filtrado.data.progre[j] = source_historicos.data.progre[i];
        source_historicos_filtrado.data.fecha[j] = source_historicos.data.fecha[i];
        source_historicos_filtrado.data.vehi[j] = source_historicos.data.vehi[i];
        source_historicos_filtrado.data.estado[j] = source_historicos.data.estado[i];
        j++;
    }
}

// Modifica el source de la tabla y la muestra nuevamente con los cambios realizados en la misma
data_table.source = source_historicos_filtrado;
data_table.visible = true;
