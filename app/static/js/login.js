function validar(){
    try{
        var email = document.getElementById("email").value;
        if(email == null || email == ""){
            alert("O e-mail não pode ser nulo!");
            return;
        }
        var email = document.getElementById("email").value;
        if(email == null || email == ""){
            alert("O e-mail não pode ser nulo!");
            return;
        }
        if(email.indexOf("@") < 1){
            alert("E-mail inválido! Digite um e-mail com '@'");
            return;
        }
        if(email.indexOf(".") < 1){
            alert("E-mail inválido! Digite um e-mail com pelo menos um '.' ");
            return;
        }

        var senha = document.getElementById("senha").value;
        if(senha == null || senha == ""){
            alert("A senha não pode ser nula!");
            return;
        }
        if(senha.length < 6){
            alert("A senha precisa ter pelo menos 6 dígitos!");
            return;
        }

        alert("Login validado com sucesso!");
    } catch(err){
        alert("Erro: " + err);
    }
}
