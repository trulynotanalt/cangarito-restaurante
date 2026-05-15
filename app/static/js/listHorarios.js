const diasSemanaMinimized = document.getElementById('dias-semana-minimized')
const diasSemanaExpand = document.getElementById('dias-semana-expand')
const barraPesquisa = document.getElementById('barra-pesquisa')

const heightDispositive = window.screen.height;
const widthDispositive = window.screen.width;
const heightNavegador = window.innerHeight;
const widthNavegador = window.innerWidth;


diasSemanaMinimized.addEventListener('click', () =>{
    const aberto = diasSemanaExpand.classList.toggle('open');
    
    let tempoTimeout = aberto ? 10 : 300
    let timeoutIDAberto = setTimeout(() => {
    if (aberto){
        diasSemanaMinimized.style.borderRadius = '16px 16px 0 0';
    }else {
        diasSemanaMinimized.style.borderRadius = '16px';
        barraPesquisa.style.marginTop = '40px'
    }
    }, tempoTimeout);
})

