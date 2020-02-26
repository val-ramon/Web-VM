var s_data = source.data;
var s_data_respaldo = source2.data;
var select_vals = cb_obj.active.map(function(x){return cb_obj.labels[x];});
var nan = NaN;
for (var i = 0; i < s_data_respaldo.x.length; i++){
    if(!isNaN(s_data.RT[i][0])){
        s_data_respaldo.x[i].fill(s_data.RT[i][0]);
    }
}
var x_respaldo = s_data.RT;
for (var i = 0; i < s_data.RT.length; i++) {
    if (!(select_vals.includes(labs[0]))){
        x_copia = s_data.RT.slice();
        s_data.RT[i].fill(nan);
        s_data.RT_intensity[i].fill(nan);
    }
    else{
        if (isNaN(x_respaldo[i][0])){
            s_data.RT[i].fill(s_data_respaldo.x[i][0]);
        }
        else{
            s_data.RT[i].fill(x_respaldo[i][0]);
        }
        s_data.RT_intensity[i] = [];
        for (var j = 0; j < 50; j++){
            s_data.RT_intensity[i].push(j);
        }
    }
}
source_respaldo = source;
source.change.emit();
console.log("callback completed");