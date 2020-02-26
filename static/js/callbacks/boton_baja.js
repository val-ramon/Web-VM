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