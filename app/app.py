from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)




@app.route('/')
def landingpage():
    #boa sorte bd.py, vulgo joão victor noberto tomaz santana
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    return render_template('landing-page.html')

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():

    #cara do bd.py q se vire aq
    # if 'roro' in session:
    #     return redirect(url_for('landingpage'))
    
    if request.method == 'POST':
        #aq o cara do banco de dados vai usar essas infos para fazer a confirmação e integração com o bd.py
        email = request.form.get('email')
        senha = request.form.get('senha')
        c_senha = request.form.get('c_senha')



    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET','POST'])
def login():

    #é necessario o cara de bd.py ai, se n eu faço tudo sozinho e ele n quer isso
    # if 'roro' in session:
    #     return redirect(url_for('landingpage'))
    
    if request.method == 'POST':
        #aq o cara do banco de dados vai usar essas infos para fazer a confirmação e integração com o bd.py
        email = request.form.get('email')
        senha = request.form.get('senha')

        
        #coisas para o cara do bd.py se preocupar em botar, n se esqueça do else
        # if roro and roro['email'] == email and roro['senha'] == senha:
        #     session['user'] = email
        #     session['id'] = roro['id']


    return render_template('login.html')


@app.route('/cardapio')
def cardapio():

    #ia esquecendo esse
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    
    return render_template('cardapio.html')

@app.route('/carrinho')
def carrinho():

    #aq tbm tem q mexer coisa linda
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    
    return render_template('carrinho.html')

@app.route('/happyhour')
def happyhour():

    #acaba nunca, avemaria
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    
    return render_template('happyhour.html')


@app.route('/perfil')
def perfil():

    #ainda bem q acabou, eu acho
    # if 'roro' not in session:
    #     return redirect(url_for('cadastro'))
    
    return render_template('perfil.html')

if __name__ == "__main__":
    app.run(debug=True)