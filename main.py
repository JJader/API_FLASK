import os

from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import json

from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

#tabelas
class Rotas(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return ("id: " + str(self.id)) 

class Turnos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return ("id: " + str(self.id))

class Veiculos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return ("id: " + str(self.id))

class Expediente(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    motorista = db.Column(db.String(100), nullable = False)
    turno = db.Column(db.String(100), nullable = False)
    rota = db.Column(db.String(100), nullable = False)
    veiculo = db.Column(db.String(100), nullable = False)
    nota = db.Column(db.Text, nullable = True)
    
    def __repr__(self):
        return ("id: " + str(self.id) + "Motorista: " + str(self.motorista))

class Alunos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(100), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    escola = db.Column(db.String(100), nullable = False)
    turno = db.Column(db.String(100), nullable = False)
    presenca = db.Column(db.Integer, nullable = False)
    id_ponto = db.Column(db.Integer, db.ForeignKey('pontos.id'), nullable = False)
    
    
    def __repr__(self):
        return ("id: " + str(self.id) + "Nome: " + str(self.nome))

class Pontos(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.String(100), nullable = False)
    alunos = db.relationship('Alunos', backref = 'aluno_id')
    lat = db.Column(db.Float, nullable = True)
    lon = db.Column(db.Float, nullable = True)
    

    def __repr__(self):
        return ("id: " + str(self.id) + " Valor: " + str(self.value))

class Chegadas(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    value = db.Column(db.String(100), nullable = False)
    status = db.Column(db.Integer, nullable = False)
    lat = db.Column(db.Float, nullable = True)
    lon = db.Column(db.Float, nullable = True)
    

    def __repr__(self):
        return ("id: " + str(self.id) + " Valor: " + str(self.value))

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    password = db.Column(db.String(100), nullable = False)
    user = db.Column(db.String(100), nullable = False)
    nome = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return ("id: " + str(self.id) + " User: " + str(self.user))

#Schema
class Rota_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rotas

class Turno_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Turnos

class Veiculo_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Veiculos

class Aluno_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alunos

class Ponto_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pontos

class Chegada_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chegadas
#rotinas
@app.route('/rotas.json')
def get_rotas():
    data = Rotas.query.all()
    rota_json = Rota_Schema()
    
    output = []
    
    for elem in data:
        elem_json = rota_json.dump(elem)
        output.append(elem_json)
    
    x = {'rotas' : output }
    return jsonify(x),200


@app.route('/turnos.json')
def get_turno():
    data = Turnos.query.all()
    turno_json = Turno_Schema()
    
    output = []
    
    for elem in data:
        elem_json = turno_json.dump(elem)
        output.append(elem_json)

    x = {'turnos' : output }
    return jsonify(x),200

@app.route('/veiculos.json')
def get_veiculo():
        data = Veiculos.query.all()
        veiculo_json = Veiculo_Schema()
        
        output = []
        
        for elem in data:
            elem_json = veiculo_json.dump(elem)
            output.append(elem_json)

        x = {'veiculos' : output }
        return jsonify(x),200


def conf_aluno(aluno_query):
    data = aluno_query.copy()
    aluno_json = Aluno_Schema()
   
    output = []

    for elem in data:
        elem_json = aluno_json.dump(elem)
        output.append(elem_json)
    x = {'alunos' : output }

    return x.copy()


@app.route('/alunos.json', methods = ['POST', 'GET'])
def get_aluno():
    if request.method == 'GET':
        
        data = Alunos.query.all()
        x = conf_aluno(data)
        
        return jsonify(x),200
        

def modifica_presenca(id, presenca):

    aluno = Alunos.query.filter_by(id = id).first()
    aluno.presenca = presenca
    db.session.commit()


@app.route('/pontos.json', methods = ['POST', 'GET'])
def conf_ponto():
    if request.method == 'GET':
        
        data = Pontos.query.all()
        ponto_json = Ponto_Schema()
        
        output = []
        
        for elem in data:
            elem_json = ponto_json.dump(elem)

            elem_json['alunos'] = conf_aluno(elem.alunos)['alunos']
            output.append(elem_json)

        x = {'pontos' : output }
        return jsonify(x),200

    elif request.method == 'POST':

        alunos_embarcados = request.get_json()
        print(alunos_embarcados)

        for aluno in alunos_embarcados['alunos']:
            id = aluno['id']
            presenca = aluno['presenca']
            modifica_presenca(id, presenca)

        
        return '1',200


@app.route('/chegada.json', methods = ['POST', 'GET'])
def conf_chegada():
    if request.method == 'GET':
        
        data = Chegadas.query.all()
        chegada_json = Chegada_Schema()
        
        output = []
        
        for elem in data:
            elem_json = chegada_json.dump(elem)

            #elem_json['alunos'] = conf_aluno(elem.alunos)['alunos']
            output.append(elem_json)

        x = {'chegadas' : output }
        return jsonify(x),200

    elif request.method == 'POST':
        """
            {
                id : 
                status : 
            }
        """
        data = request.get_json()
        print(atualizacao_chegada)
        
        id = data['id']
        status = data['status']
        
        chegada = Chegadas.query.filter_by(id = id).first()
        chegada.status = status
        db.session.commit()

        
        return '1',200


@app.route('/registrar/rota', methods = ['POST'])
def set_rota():
    retorno = {'ok': True}

    data = request.get_json()
    print(data)
    new_expediente = Expediente(
        motorista = data['id'],
        turno = data['turno'],
        rota = data['rota'],
        veiculo = data['veiculo'],
        nota = data['nota']
    )
    db.session.add(new_expediente)
    #db.session.add(Blog_post.query.get(id))
    db.session.commit()

    return jsonify(retorno), 200

def verify_password(username, password):
    user = Usuarios.query.filter_by(user = username).first()
    if user and user.password == password:
            return (True, user)

    return (False, None)
    
    
@app.route('/login', methods = ['POST', 'GET'])
def validar_usuario():

    data = request.get_json()
    
    username = data['user']
    password = data['password']
    
    if username is None or password is None:
        return jsonify(-1) , 404
    
    (validation ,user) = verify_password(username, password)
    
    if validation :
        print(user)
        retorno = {'id' : user.id, 'nome' : user.nome} 
        return jsonify(retorno),200
    else:
        return jsonify(-1), 404
    
if __name__ == "__main__":
    db.create_all()
    os.system("clear")
    app.run(host = '0.0.0.0',use_reloader= True, debug= True)
    
