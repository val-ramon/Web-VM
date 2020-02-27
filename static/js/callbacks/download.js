// Primero crea una funcion que sirve para transformar un data source en un string con formato para csv
function table_to_csv(source) {
    /*Esta funcion columna por columna y las concatena con comas, a su vez concatena cada fila con saltos de linea,
        esto es para poder lograr un formato legible y crear un archivo csv.*/
    var columns = Object.keys(source.data);
    const nrows = source.get_length();
    var lugar = columns.indexOf("RT_intensity");
    columns.splice(lugar, 1);
    lugar = columns.indexOf("index");
    columns.splice(lugar, 1);
    var lines = [columns.join(',')];
    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j];
            if (column !== "RT_intensity"){
                if (column !== "ProgresivaFin" && column !== "ProgresivaIni" && column !== "RT"){
                    row.push((source.data[column][i].toString()).replace(/,/g, "/"));
                }
                else if (column === "RT"){
                    row.push(source.data[column][i][0].toString());
                }
                else{
                    row.push(source.data[column][i].toString());
                }
            }
        }
        lines.push(row.join(','));
    }
    return lines.join('\\n').concat('\\n');
}

// Crea el archivo csv con los datos de las zonas para poder descargarlo desde el navegador
const filename = 'change_emmited.csv';
var filetext = table_to_csv(source);
filetext = filetext.slice(0, filetext.length - 1);
const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

// Crea un objeto de URL para poder descargar el archivo con los datos de la zonas
//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}
else {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.target = '_blank';
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'));
}

console.log("callback completed");
