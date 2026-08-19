from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel # importando a classe do arquivo hotel dentro da pasta resources.
from resources.site import Sites, Site #importando as classes do arquivo site.py dentro da pasta resources
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
# O postman é o correlativo do Hoppscotch. Ele serve só pra testar as requisições que o
#frontend faria. Testando a troca de JSON, que é o pacote de dados enviado entre front
# e back, passando pela API.
#Quando o Terraform sobe os codigos pro GCP e o Apigee está configurado (responsavel
# pela api, controla os JSONs no GCP), o Postman sai de cena, quem faz agora a requisiçao
# de endpoint pro backend é o front 

#Configurações do Flask:
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #configurando o caminho do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Configuração pra ele nao ficar mostrando mensagem 
app.config['JWT_SECRET_KEY'] = 'api-python' #para lidar com token de acesso do json precisa configurar uma chave de segurança
app.config['JWT_BLACKLIST_ENABLED'] = True #Estamos ativando a BLACKLIST do JWT, para invalidar token ID em caso de logout.
api = Api(app) #configuração da comunicação app com API
jwt = JWTManager(app)

@app.before_request #Decorador pra atuar antes de qualquer requisição da API
def cria_banco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_token_na_blocklist(jwt_header, jwt_payload):
    # return token['jti'] in BLACKLIST
    jti = jwt_payload['jti']
    return jti in BLOCKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidado(jwt_header, jwt_payload):
    return jsonify({'message': 'You have been logged out.'}), 401 # unauthorized


#Aqui justamente eu defino os recursos que existem na minha API que o meu Backend vai esperar receber e manipular. Endpoint é requisição do front ao back.
api.add_resource(Hoteis, '/hoteis') #adicionando nosso recurso. '/hoteis' acessa todos hoteis da api.
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') #adicionando recurso Hotel linkado ao endpoint /hoteis e /hotel_id
api.add_resource(Sites, '/sites') #adicionando recurso Sites (get) definidos no arquivo site.py dentro da pasta recursos.
api.add_resource(Site, '/sites/<string:url>') #adicionando o recurso Site (classe herdada da classe Mae Resources para o flask)
api.add_resource(User, '/usuarios/<int:user_id>') #adicionando recurso User ao endpoint '/usuarios' e em seguida '/user_id'
api.add_resource(UserRegister, '/cadastro') #Adicionando recurso de cadastro de usuario UserRegister ao endpoint
api.add_resource(UserLogin, '/login') #Adicionando recurso login de usuario ao endpoint '/login'.
api.add_resource(UserLogout, '/logout')


#configurações básicas do Flask:
if __name__ == '__main__': #se for o arquivo app.py
    from sql_alchemy import banco # eu nao quero que esse banco init seja executado se for chamado de outro arquivo
    banco.init_app(app) 
    app.run(debug=True)

#Até aqui: estamos criando o seguinte recurso: http://127.0.0.1:5000/hoteis
# Essa é a raiz do site: http://127.0.0.1:5000 