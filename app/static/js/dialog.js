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

      <div class="container-observacao">
        <h2>Alguma Observação?</h2>
        <textarea name="observacao-dialog" id="observacao-dialog"></textarea>
      </div>

      <div class="footer-dialog">
        <div class="widget-quantidade">
          <button type="button" class="diminuir-quantidade">-</button>
          <input type="text" name="quantidade-atual-widget" class="quantidade-atual-widget" value="0">
          <button type="button" class="aumentar-quantidade">+</button>
        </div>
        <button class="adicionar-dialog">Adicionar + ${preco}</button>
      </div>
    `;

    dialog.showModal();
    const botaoAumentar = document.querySelector('.aumentar-quantidade');
    const botaoDiminuir = document.querySelector('.diminuir-quantidade');
    const quantidadeAtualInput = document.querySelector('.quantidade-atual-widget');
    
    botaoAumentar.addEventListener('click', ()=>{
      let valorAtual  = parseInt(quantidadeAtualInput.value) || 0
      quantidadeAtualInput.value = valorAtual + 1
    })
    
    botaoDiminuir.addEventListener('click', ()=>{
      let valorAtual  = parseInt(quantidadeAtualInput.value) || 0
      valorAtual -= 1
      if (valorAtual < 0){
        return
      }
      quantidadeAtualInput.value = valorAtual 
    })
    const fecharBtn = dialog.querySelector('#fechar-dialog');
    fecharBtn.addEventListener('click', () => {
      dialog.close();
    });
  });
});
