var s_data = source.data;
var data = cb_obj.value;
var nueva_data = source3.data;
var indice = s_data.Intensity_tip.indexOf(nueva_data.zona[0]);

s_data.rel_int[indice] = data.toFixed(2);
source.change.emit();
console.log("callback completed");