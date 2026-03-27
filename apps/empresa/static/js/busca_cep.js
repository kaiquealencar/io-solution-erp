document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('cep');
    
    function buscarEndereco() {
        const cep = cepInput.value.replace(/\D/g, '');
        var logradouroInput = document.getElementById('logradouro');
        var bairroInput = document.getElementById('bairro');
        var cidadeInput = document.getElementById('cidade');
        var estadoInput = document.getElementById('estado');

        if (cep.length === 8) {
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        logradouroInput.value = data.logradouro || '';
                        bairroInput.value = data.bairro || '';
                        cidadeInput.value = data.localidade || '';
                        estadoInput.value = data.uf || '';

                      


                        document.getElementById('numero').focus();
                    } else {
                        alert('CEP não encontrado.');
                    }
                })
                .catch(error => console.error('Erro ao buscar CEP:', error));
        }
    }

    cepInput.addEventListener('blur', buscarEndereco);

    cepInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            buscarEndereco();
        }
    });
});