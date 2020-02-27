// Los sources y la tabla llegan desde Python pasados por parametros

var id = cb_obj['value_input']; // Toma en tiempo real lo escrito en el input de filtrado de id y lo asigna a una variable
source_filtros.data.id[0] = id; // Le asigna ese id al source de filtros para poder guardarlo
data_table.visible = false; // Oculta momentaneamente la tabla para simular actualizacion de datos en tiempo real

// Elimina todos los datos del source de historicos filtrados para evitar un conflicto al sobreescribir datos
var j = 0;
source_historicos_filtrado.data.id = [];
source_historicos_filtrado.data.progre = [];
source_historicos_filtrado.data.fecha = [];
source_historicos_filtrado.data.vehi = [];
source_historicos_filtrado.data.estado = [];

// Recorre todo el source para ver cuales son los eventos que tienen el id correspondiente al filtrado, en caso de no haber ninguno, muestra todos
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

// Setea el nuevo source a la tabla y la muestra nuevamente
data_table.source = source_historicos_filtrado;
data_table.visible = true;
