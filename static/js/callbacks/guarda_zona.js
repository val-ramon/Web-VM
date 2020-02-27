var f = cb_obj.value; // Con cb_obj se obtiene el valor del select
var zona = source3.data.zona; // Toma el valor de zona que esta en el source que llega desde Python
zona[0] = f; // Le asigna el nuevo valor de zona tomado desde el select para poder usarlo despues
source3.change.emit(); // Le avisa al source mediante esta linea que debe emitir un cambio
console.log("callback completed");
