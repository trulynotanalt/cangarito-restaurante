from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)




@app.route('/')
def landingpage():
    return render_template('landing-page.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/happyhour')
def happyhour():
    return render_template('happyhour.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

if __name__ == "__main__":
    app.run(debug=True)