function validar() {
    try {
        
        var campoNome = document.getElementById("nome") || document.getElementById("usuario");
        if (campoNome) {
            var nome = campoNome.value.trim();
            if (nome === null || nome === "") {
                alert("O nome de usuário não pode ser vazio!");
                return false; // Impede o envio do formulário
            }
        }

  
        var campoEmail = document.getElementById("email");
        if (campoEmail) {
            var email = campoEmail.value.trim();
            if (email === null || email === "") {
                alert("O e-mail não pode ser nulo!");
                return false;
            }
            if (email.indexOf("@") < 1) {
                alert("E-mail inválido! Digite um e-mail com '@'");
                return false;
            }
            if (email.indexOf(".") < 1) {
                alert("E-mail inválido! Digite um e-mail com pelo menos um '.'");
                return false;
            }
        }

    
        var campoSenha = document.getElementById("senha");
        if (campoSenha) {
            var senha = campoSenha.value;
            if (senha === null || senha === "") {
                alert("A senha não pode ser nula!");
                return false;
            }
            if (senha.length < 6) {
                alert("A senha precisa ter pelo menos 6 dígitos!");
                return false;
            }
        }

      
        var campoRepSenha = document.getElementById("repsenha");
        if (campoRepSenha) {
            var repSenha = campoRepSenha.value;
            if (senha !== repSenha) {
                alert("As senhas não coincidem!");
                return false;
            }
        }

        
        return true; 
    } catch(err) {
        alert("Erro na validação: " + err);
        return false;
    }
}

