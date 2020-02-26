var label = cb_obj['label'];
var nueva_data = select.value;
var indice = source.data.Intensity_tip.indexOf(nueva_data);
var j = 9;
var data_source_historicos_muestra = source_historicos_muestra.data;
data_source_historicos_muestra.progre = [];
data_source_historicos_muestra.id = [];
data_source_historicos_muestra.vehi = [];
data_source_historicos_muestra.fecha = [];
data_source_historicos_muestra.estado = [];
if (label === 'Mostrar ultimos eventos de zona'){
    for (var i = source_eventos.data.progre.length - 1; i >= 0; i--){
        if (parseInt(source_eventos.data.progre[i]) >= parseInt(source.data.ProgresivaIni[indice].split('pk')[1]) && (source_eventos.data.progre[i] <= parseInt(source.data.ProgresivaFin[indice].split('pk')[1])) && j >= 0){
            data_source_historicos_muestra.progre[j] = source_eventos.data.progre[i];
            data_source_historicos_muestra.id[j] = source_eventos.data.id[i];
            data_source_historicos_muestra.vehi[j] = source_eventos.data.vehi[i];
            data_source_historicos_muestra.fecha[j] = source_eventos.data.fecha[i];
            data_source_historicos_muestra.estado[j] = source_eventos.data.estado[i];
            j--;
        }
    }
    source_historicos_muestra.change.emit();
    dataTable.source = source_historicos_muestra;
    dataTable.visible = true;
    div2.visible = true;
    cb_obj['label'] = 'Ocultar ultimos eventos de zona';
}
else{
    dataTable.visible = false;
    div2.visible = false;
    cb_obj['label'] = 'Mostrar ultimos eventos de zona';
}