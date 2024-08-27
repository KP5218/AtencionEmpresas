$(document).ready(function(){
            // Maneja el clic en los enlaces
            $('.nav-link').on('click', function(){
                // Quita la clase activa de todos los enlaces
                $('.nav-link').removeClass('active');
                // Agrega la clase activa solo al enlace clickeado
                $(this).addClass('active');
            });
        });