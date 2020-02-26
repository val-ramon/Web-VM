var f = cb_obj.value;
var zona = source3.data.zona;
zona[0] = f;
source3.change.emit();
console.log("callback completed");