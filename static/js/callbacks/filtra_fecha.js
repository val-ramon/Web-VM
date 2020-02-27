// Los sources y la tabla llegan como parametros desde Python

var estado = source_filtros.data.estado[0]; // Toma los estados grabado en el source de filtros para poder filtrar
var value_slider = source_filtros.data.rango_pk[0]; // Toma los valores del rango de progresivas

// Toma las fechas del source de filtros, la separa por barras y las transforma en formato Date para poder realizar operaciones
var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));

data_table.visible = false; // Oculta la tabla momentaneamente para poder simular actualizacion en tiempo real

/* Vacia el source de datos filtrado para evitar inconvenientes con el agregado de nuevos datos*/
var j = 0;
source_historicos_filtrado.data.id = [];
source_historicos_filtrado.data.progre = [];
source_historicos_filtrado.data.fecha = [];
source_historicos_filtrado.data.vehi = [];
source_historicos_filtrado.data.estado = [];

// Recorre todo el source de datos de la base de datos para encontrar las coincidencias y filtrarlos sobre los criterios dados
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

// Modifica el source de la base de datos y muestra nuevamente la tabla para poder visualizar los nuevos datos en la tabla
data_table.source = source_historicos_filtrado;
data_table.visible = true;
