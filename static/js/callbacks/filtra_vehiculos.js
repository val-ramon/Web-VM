// Los sources vienen como parametros desde Python mediante la funcion CustomJS, donde se pasan los parametros como diccionarios

var value_slider = source_filtros.data.rango_pk[0]; // Recibe valores del range slider para poder filtrar
var data = cb_obj.active.map(function(x){ return cb_obj.labels[x];}); // Mapea las celdas seleccionadas en el checkbox para poder buscar y filtrar
source_filtros.data.vehiculo[0] = data; // Le asigna la data de los vehiculos al source de filtros para poder utilizarlo en los demas filtros

// Toma los valores de string de fechas, las separa por las barras y la convierte a formato Date para poder trabajar con ellas
var fechaIni = new Date(source_filtros.data.rango_fecha[0][0].split('/'));
var fechaFin = new Date(source_filtros.data.rango_fecha[0][1].split('/'));

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

// Al terminar esto, se le asigna la nueva data a la tabla y se la vuelve a mostrar nuevamente
data_table.source = source_historicos_filtrado;
data_table.visible = true;
