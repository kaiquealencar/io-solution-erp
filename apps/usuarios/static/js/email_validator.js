document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.querySelector('#email');
    const msgContainer = document.querySelector('#email-msg');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            const email = emailInput.value.trim();

            if (email !== "") {
                fetch('/usuarios/validar-email/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken
                    },
                    body: `email=${encodeURIComponent(email)}`
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => { throw err; });
                    }
                    return response.json(); 
                })
                .then(data => {
                    msgContainer.classList.remove('opacity-0');
                    msgContainer.classList.add('opacity-100');

                    if (data.valid) {
                        msgContainer.innerHTML = '✔ Disponível';
                        msgContainer.className = "text-xs mt-1 block text-green-600 font-medium opacity-100 transition-opacity duration-500";
                    } else {
                        msgContainer.innerHTML = '✖ ' + (data.error || 'E-mail já cadastrado.');
                        msgContainer.className = "text-xs mt-1 block text-red-600 font-medium opacity-100 transition-opacity duration-500";
                        emailInput.value = '';
                    }

                    setTimeout(() => {
                        msgContainer.classList.replace('opacity-100', 'opacity-0');

                        setTimeout(() => {
                            if (msgContainer.classList.contains('opacity-0')) {
                                msgContainer.innerHTML = '';
                            }
                        }, 500);
    
                    }, 3000); 
                })
                .catch(error => {
                    console.error('Erro na requisição:', error);
                });
            }
        });
    }
});