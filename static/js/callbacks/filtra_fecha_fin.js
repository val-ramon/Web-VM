// Toma el valor del input ingresado donde se filtra por fecha final y se lo asigna al source de filtros que llega como parametro desde Python

var fecha_fin = cb_obj['value_input'];
source_filtros.data.rango_fecha[0][1] = fecha_fin;
