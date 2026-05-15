const themeWidget = document.getElementById('theme-widget');

function setTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}


const savedTheme = localStorage.getItem('theme') || 'light';
setTheme(savedTheme);


themeWidget.addEventListener('click', () => {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
});
