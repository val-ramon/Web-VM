// El source llega como parametro desde Python

// Crea una funcion range ya que en JS no existe dicha funcion
function range(start, end) {
    var ans = [];
    for (let i = start; i <= end; i++) {
        ans.push(i);
    }
    return ans;
}

// Obliba al source a mantener sus coordenadas en y para que no se puedan ir las lineas de las zonas de la figura
for (var j = 0; j < source.data.RT.length; j++){
    source.data.RT_intensity[j] = range(0, 49);
}

source.change.emit(); // Aplica los cambios al source
