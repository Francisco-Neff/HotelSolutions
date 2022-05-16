function reservaHabitacion(id_habtitacion){
    //Campos para la petición POST
    var reserva = {
        id_habitacion: id_habtitacion,
        fx_entrada: $('#entrada').text(),
        fx_salida: $('#salida').text(),
        nombre: $('#id_nombre').val(),
        apellido: $('#id_apellido').val(),
        email: $('#id_email').val()
    }
    
       
        var frm = $('#contacform');
        if (reserva.apellido.length != 0 && reserva.nombre.length != 0 && reserva.email  != 0){ 
          if (IsEmail(reserva.email)) {
        
            $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "X-Requested-With": "XMLHttpRequest"
                },
            data: reserva,
            success: function(){
                alert('success');
                },
                error: function(){
                    alert('failure');
                }
             });}
             
          else { 
              alert('El email no esta en un formato correcto')
          }}
        else {
            alert('Debes rellenar todos los campos.')}
        }