document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.querySelector('#email');
    const msgContainer = document.querySelector('#email-msg');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    if (emailInput && msgContainer) {
        emailInput.addEventListener('blur', function() {
            const emailAtual = emailInput.value.trim();
            const emailOriginal = emailInput.getAttribute('data-original')?.trim();


            if (emailAtual === "" || emailAtual === emailOriginal) {
                console.log("Sem alteração ou vazio. Abortando validação.");
                msgContainer.classList.replace('opacity-100', 'opacity-0');
                return; 
            }

            fetch('/usuarios/validar-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `email=${encodeURIComponent(emailAtual)}`
            })
            .then(response => response.json())
            .then(data => {
                msgContainer.classList.remove('opacity-0');
                msgContainer.classList.add('opacity-100');

                if (data.valid) {
                    msgContainer.innerHTML = '✔ Disponível';
                    msgContainer.className = "text-xs mt-1 block text-green-600 font-medium opacity-100 transition-opacity duration-500";
                } else {
                    msgContainer.innerHTML = '✖ ' + (data.error || 'E-mail já cadastrado.');
                    msgContainer.className = "text-xs mt-1 block text-red-600 font-medium opacity-100 transition-opacity duration-500";
                    emailInput.value = ''; // Apaga se for inválido
                }

                setTimeout(() => {
                    msgContainer.classList.replace('opacity-100', 'opacity-0');
                }, 3000);
            })
            .catch(error => console.error('Erro:', error));
        });
    }
});