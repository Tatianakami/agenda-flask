from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
import re

# variáveis de ambiente
load_dotenv()

# Configuração do aplicativo
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'uma-chave-secreta-padrao')

# Proteção CSRF
csrf = CSRFProtect(app)

#  banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#  Contato
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

def validar_telefone(telefone):
    """Valida o formato do telefone"""
    padrao = re.compile(r'^\+?[\d\s-]{8,15}$')
    return bool(padrao.match(telefone))

# Rotas
@app.route('/')
def index():
    contatos = Contato.query.order_by(Contato.nome).all()
    return render_template('index.html', contatos=contatos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    try:
        nome = request.form.get('nome', '').strip()
        telefone = request.form.get('telefone', '').strip()
        
        # Validação
        if not nome or len(nome) > 100:
            flash('Nome inválido. Deve ter entre 1 e 100 caracteres.', 'error')
            return redirect(url_for('index'))
            
        if not validar_telefone(telefone):
            flash('Telefone inválido. Use um formato válido.', 'error')
            return redirect(url_for('index'))
            
        if Contato.query.filter_by(telefone=telefone).first():
            flash('Este telefone já está cadastrado.', 'error')
            return redirect(url_for('index'))
            
        novo_contato = Contato(nome=nome, telefone=telefone)
        db.session.add(novo_contato)
        db.session.commit()
        
        flash('Contato adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao adicionar o contato: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    try:
        contato = Contato.query.get_or_404(id)
        db.session.delete(contato)
        db.session.commit()
        flash('Contato removido com sucesso!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao remover o contato: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

        
