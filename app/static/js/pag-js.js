

function validar(){
    try{
        var usuario = document.getElementById("usuario").value;
        if (usuario == null || usuario === "") {
            alert("Digite um nome de usuário!");
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

        var repsenha = document.getElementById("repsenha").value;
        if(repsenha == ""){
            alert("A senha repetida não pode ser nula");
            return;
        }
        if(senha !== repsenha){
            alert("As senhas precisam ser idênticas");
            return;
        }

        alert("Login validado com sucesso!");
        function redirecionar() {
            window.location.href = "../../Cardápio/cardapio.html";
        }
    } catch(err){
        alert("Erro: " + err);
    }
}

