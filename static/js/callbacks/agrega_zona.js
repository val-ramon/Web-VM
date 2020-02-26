if (cb_obj.label === 'Agregar zonas'){
    cb_obj.label = 'Terminar de agregar zonas';
    text_input_prog_ini.visible = true;
    text_input_prog_fin.visible = true;
    boton_confirma_zona.visible = true;
}
else{
    cb_obj.label = 'Agregar zonas';
    text_input_prog_ini.visible = false;
    text_input_prog_fin.visible = false;
    boton_confirma_zona.visible = false;
}