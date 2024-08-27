document.addEventListener('DOMContentLoaded', function () {
        var selectTipo = document.getElementById('tipo');
        var selectMutual = document.getElementById('select_mutual');
        var selectMutualValor = document.getElementById('mutual_cliente');


        selectTipo.addEventListener('change', function () {
            selectMutual.style.display = 'none';

            if (selectTipo.value === '01') {
                selectMutual.style.display = 'block';
                selectMutualValor.setAttribute('required', 'required');

            } else if (selectTipo.value === '02') {
                selectMutualValor.value = '';
                selectMutual.style.display = 'none';
                selectMutualValor.removeAttribute('required');

            }
        });
    });
