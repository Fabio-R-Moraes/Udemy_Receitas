function meu_escopo() {
    const formularios = document.querySelectorAll('.form-delete');

    for(const formulario of formularios) {
        formulario.addEventListener('submit', function(e) {
            e.preventDefault();
            const confirmado = confirm('Você tem certeza??')

            if(confirmado) {
                formulario.submit();
            }
        })
    }
}

meu_escopo();