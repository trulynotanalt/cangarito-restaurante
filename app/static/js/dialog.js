const dialog = document.querySelector('dialog');
const produtos = document.querySelectorAll('.grade-produtos article');

produtos.forEach(produto => {
  produto.addEventListener('click', () => {
    const imgSrc = produto.querySelector('img').src;
    const nome = produto.querySelector('h3').textContent;
    const preco = produto.querySelector('h2').textContent;
    const descProduto = produto.querySelector('.desc-produto').textContent;
    

    dialog.innerHTML = `
  <div id="header-dialog">
    <span class="sair-dialog">
      <i id="fechar-dialog" class="bi bi-chevron-compact-down"></i>
    </span>
    <h1>${nome}</h1>
  </div>

  <div class="container-dialog">
    <img src="${imgSrc}" alt="">

    <div class="info-dialog">
      <div class="container-tags-produto">
        <div class="tags-produto"><p>300g</p></div>
        <div class="tags-produto"><p>300g</p></div>
        <div class="tags-produto"><p>300g</p></div>
      </div>

      <p class="desc-produto">${descProduto}</p>
    </div>
  </div>

  

  <form method="POST" action="/cardapio">

    <div class="container-observacao">
      <h2>Alguma Observação?</h2>
      <textarea name = "observacao" id = "observacao-dialog"></textarea>
    </div>

    <input
      type="hidden"
      name="nome_produto"
      value="${nome}">

    <input
      id="item_quantidade_input"
      type="hidden"
      name="quantidade_pedido"
      value="1">

    <div class="footer-dialog">

      <div class="widget-quantidade">
        <button type="button" class="diminuir-quantidade">-</button>

        <input
          type="text"
          class="quantidade-atual-widget"
          value="1">

        <button type="button" class="aumentar-quantidade">+</button>
      </div>

      <button type="submit" class="adicionar-dialog">
        Adicionar + ${preco}
      </button>

    </div>

  </form>
`;

    dialog.showModal();
    const botaoAumentar = dialog.querySelector('.aumentar-quantidade');
    const botaoDiminuir = dialog.querySelector('.diminuir-quantidade');
    const quantidadeAtualInput = dialog.querySelector('.quantidade-atual-widget')
    const quantidadePedido     = dialog.querySelector('#item_quantidade_input');
    
    botaoAumentar.addEventListener('click', () => {
    let valorAtual = parseInt(quantidadeAtualInput.value) || 0;
    valorAtual++;

    quantidadeAtualInput.value = valorAtual;
    quantidadePedido.value = valorAtual;
    });

    botaoDiminuir.addEventListener('click', ()=>{
      let valorAtual  = parseInt(quantidadeAtualInput.value) || 0
      
      if (valorAtual>1){
        valorAtual--;

        quantidadeAtualInput.value = valorAtual;
        quantidadePedido.value = valorAtual;
      }
    });
    const fecharBtn = dialog.querySelector('#fechar-dialog');
    fecharBtn.addEventListener('click', () => {
    dialog.close();
    });
  });
});

