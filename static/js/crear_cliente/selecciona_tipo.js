document.addEventListener('DOMContentLoaded', function () {
        var selectTipo = document.getElementById('tipo');
        var div_empresa = document.getElementById('div_empresa');
        var div_mutual = document.getElementById('div_mutual');
        var selectMutualValor = document.getElementById('mutual_cliente');
        var selectEmpresaValor = document.getElementById('empresa_cliente');
        var div_utms = document.getElementById('div_utms');
        var selectUtmsValor = document.getElementById('utms_cliente');


        selectTipo.addEventListener('change', function () {

            if (selectTipo.value === '01') { //esto es empresa
                div_mutual.style.display = 'none';
                selectMutualValor.removeAttribute('required');

                div_utms.style.display = 'none';
                selectUtmsValor.removeAttribute('required');

                div_empresa.style.display = 'block';
                selectEmpresaValor.setAttribute('required', 'required');

                selectMutualValor.value = '';
                selectUtmsValor.value = '';

            } else if (selectTipo.value === '02') { //esto es mutual
                div_empresa.style.display = 'none';
                selectEmpresaValor.removeAttribute('required');

                div_utms.style.display = 'none';
                selectUtmsValor.removeAttribute('required');

                div_mutual.style.display = 'block';
                selectMutualValor.setAttribute('required', 'required');

                selectEmpresaValor.value = '';
                selectUtmsValor.value = '';

            } else if (selectTipo.value === '03') { //esto es utms
                div_empresa.style.display = 'none';
                selectEmpresaValor.removeAttribute('required');

                div_mutual.style.display = 'none';
                selectMutualValor.removeAttribute('required');

                div_utms.style.display = 'block';
                selectUtmsValor.setAttribute('required', 'required');

                selectMutualValor.value = '';
                selectEmpresaValor.value = '';

            }
        });
    });
