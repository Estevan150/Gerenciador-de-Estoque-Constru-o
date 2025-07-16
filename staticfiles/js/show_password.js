// Arquivo: static/js/show_password.js

// Espera a página carregar completamente antes de rodar o script
window.addEventListener("load", function() {
    // Os campos de senha no admin do Django têm IDs específicos.
    // id_password1 é o campo da nova senha.
    // id_password2 é o campo de confirmação da senha.
    const passwordFieldIDs = ['#id_password1', '#id_password2'];

    passwordFieldIDs.forEach(function(fieldId) {
        const passwordInput = document.querySelector(fieldId);

        // Se o campo de senha existir na página atual...
        if (passwordInput) {
            // Cria um botão
            const button = document.createElement('button');
            button.innerHTML = '👁️'; // Ícone de olho
            button.type = 'button';
            button.classList.add('btn', 'btn-outline-secondary'); // Estilo do Bootstrap

            // Adiciona o evento de clique no botão
            button.addEventListener('click', function() {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
            });

            // Envolve o campo e o botão em um 'input-group' do Bootstrap para que fiquem juntos
            const wrapper = document.createElement('div');
            wrapper.classList.add('input-group');
            passwordInput.parentNode.insertBefore(wrapper, passwordInput);
            wrapper.appendChild(passwordInput);
            wrapper.appendChild(button);
        }
    });
});