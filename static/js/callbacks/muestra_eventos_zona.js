// El select, la tabla, el div (division en HTML para poder plasmar algo) y los sources llegan desde Python

var label = cb_obj['label']; // Se fija el label del boton para mostrar ultimos eventos de la zona
var nueva_data = select.value; // Se fija el valor del select para poder saber en que zona esta
var indice = source.data.Intensity_tip.indexOf(nueva_data); // Busca el indice donde se encuentra dicha zona
var j = 9;

var data_source_historicos_muestra = source_historicos_muestra.data; // Guarda la data del source que contiene los datos historicos para poder modificarlos luego

// Vacia los arrays del source de historicos para que no haya conflictos al sobreescribir
data_source_historicos_muestra.progre = [];
data_source_historicos_muestra.id = [];
data_source_historicos_muestra.vehi = [];
data_source_historicos_muestra.fecha = [];
data_source_historicos_muestra.estado = [];

/* Se fija el valor del label del boton, si es para mostrar las zonas, busca los ultimos 10 eventos comprendidos entre las progresivas de la zona
    y los asigna al source que utiliza la tabla, modifica la tabla, la muestra y modifica el boton en caso de querer ocultar los eventos.

    En caso de que el label sea la segunda opcion, simplemente oculta la tabla con los ultimos eventos.*/
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
