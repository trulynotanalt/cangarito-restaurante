function aplicarTema(theme) {
    document.body.setAttribute('data-theme', theme);
}

const temaSalvo = localStorage.getItem('theme');

if (temaSalvo) {
    aplicarTema(temaSalvo);
} else {
    aplicarTema('light');
}