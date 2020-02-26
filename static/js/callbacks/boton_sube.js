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