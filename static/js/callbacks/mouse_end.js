// Los sources, boton y herramienta de modificacion llegan desde Python pasados por parametro como diccionario

var s_data_cuadrados = source_cuadrados.data; // Toma la data del source que representa el sombreado de zonas
var s_data = source.data; // Toma la data del source original que contiene la informacion de las zonas
s_data.RT[s_data.RT.length - 1].fill(largo_ducto); // Obliga a rellenar la ultima zona con el mismo valor de x para que sea inamovible

// Recorre todo el source del sombreado para identificar los silenciados y cambiarles el color
for (var i = 0; i < s_data_cuadrados.color.length; i++){
    if (s_data.Eventos_permitidos[i].includes('Ninguno')){
        s_data_cuadrados.color[i] = 'White';
    }
    else{
        s_data_cuadrados.color[i] = 'Grey';
    }
}
source_respaldo.data = source.data; // Modifica el source de respaldo para guardar la data
s_data_cuadrados.cont[0] = 0; // Modifica el contador del source de sombreados que sirve como identificador de otras funciones
draw_tool_l1.active = false; // Desactiva la herramienta que permite modificar las zonas
boton_elimina_zona.disabled = true; // Deshabilita el boton que sirve para eliminar zonas
source_cuadrados.change.emit(); // Emite los cambios al source de sombreados
