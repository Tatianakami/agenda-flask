// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('Agenda de Contatos - JavaScript inicializado');
    
    // 1. MELHORIA NA VALIDAÇÃO DO FORMULÁRIO (CLIENT-SIDE)
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(event) {
            const telefoneInput = document.querySelector('input[name="telefone"]');
            const telefone = telefoneInput.value.trim();
            
            // Validação do telefone (opcional no cliente)
            if (!/^[\d\s-]{8,15}$/.test(telefone)) {
                alert('Por favor, insira um telefone válido (8 a 15 dígitos, pode conter hífens ou espaços)');
                telefoneInput.focus();
                event.preventDefault();
                return false;
            }
            
            // Validação do nome
            const nomeInput = document.querySelector('input[name="nome"]');
            const nome = nomeInput.value.trim();
            
            if (nome.length < 2) {
                alert('O nome deve ter pelo menos 2 caracteres');
                nomeInput.focus();
                event.preventDefault();
                return false;
            }
        });
    }
    
    // 2. CONFIRMAÇÃO PARA EXCLUSÃO
    const deleteButtons = document.querySelectorAll('.btn-danger');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este contato?')) {
                e.preventDefault();
            }
        });
    });
    
    
    // Observa mudanças na URL (para limpar campos quando um contato é adicionado)
    const observer = new MutationObserver(function(mutations) {
        if (window.location.search.includes('success')) {
            const nomeInput = document.querySelector('input[name="nome"]');
            const telefoneInput = document.querySelector('input[name="telefone"]');
            
            if (nomeInput && telefoneInput) {
                nomeInput.value = '';
                telefoneInput.value = '';
                nomeInput.focus();
            }
        }
    });
    
    observer.observe(document, {childList: true, subtree: true});
    
    // 4. MASCARÁ PARA TELEFONE (OPCIONAL)
    const telefoneInput = document.querySelector('input[name="telefone"]');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            // Formatação simples: (XX) XXXXX-XXXX
            if (value.length > 2) {
                value = `(${value.substring(0,2)}) ${value.substring(2)}`;
            }
            if (value.length > 10) {
                value = `${value.substring(0,10)}-${value.substring(10,14)}`;
            }
            
            e.target.value = value;
        });
    }
});