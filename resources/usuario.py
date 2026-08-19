from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from blocklist import BLOCKLIST

#Esse arquivo é onde eu defino a classe Usuario e o que ela faz. 

#a biblioteca do flask_restful converte automaticamente o retorno de get(self) para JSON
atributos = reqparse.RequestParser()
atributos.add_argument('login', type= str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type= str, required=True, help="The field 'senha' cannot be left blank")


#Definindo os Recursos da API: Nada mais é do que requisições que a API faz pro Backend (aqui).
class User(Resource): #Resource é a classe do flask_restful que ja ta embutido.
    
    #Recursos referentes a: endereço_raiz/usuarios/{user_id}
    def get(self, user_id): #ele recebe o user_id na chamada do get pois eu vou passar isso no endpoint, e sempre que cria um usuario o sql vai associar um valor pra ele
        user = UserModel.find_user(user_id)
        if user:
            return user.json() #o return ele sempre interrompe a função
        return {'message': 'User not found'} , 404 #Status Code HTTP Not Found
    
    @jwt_required() #So deleta usuario se tiver com token de Login (do usuario)
    def delete(self, user_id): #user id não é passado no Postman, nao tem como saber qual id eu quero deletar
        user = UserModel.find_user(user_id)
        if user:
            try: 
                user.delete_user() #Deletar o User da tabela.
                return {'message': 'User Deleted.'}
            except:
                return {'message': 'An internal error ocurred trying to delete user.'}, 500 #Código HTTP: Internal Server Error
        return {'message': 'User not found.'}, 404 # Codigo HTTP pra Not found. retorna mensagem de hotel nao encontrado
    
class UserRegister(Resource):

    #Recurso desse vai ser diferente: endereço_raiz/cadastro
    def post(self): #Ação: criar usuario.
        #recebendo os dados da requisição API
        dados = atributos.parse_args()
        user = UserModel.find_user_by_login(dados['login'])
        if user:
            return {"message": "User '{}' already exists.".format(dados['login'])}, 400 #codigo HTTP Bad request
        new_user = UserModel(**dados) #crio objeto da classe com login e senha.
        new_user.save_user()
        return {"message": "User createad successfully!"}
    
class UserLogin(Resource):
    #Ação: fazer login.
    @classmethod
    def post(cls): #me referindo a propria classe com o cls
        dados = atributos.parse_args()
        user = UserModel.find_user_by_login(dados['login'])
        if user and compare_digest(user.senha, dados['senha']): #comparar se a senha digitada é identica a senha cadastrada em dados
            token_de_acesso = create_access_token(identity=str(user.user_id)) #cria token str na variavel 'token_de_acesso'.
            return {'acccess_token': token_de_acesso}, 200 #codigo HTTP para Sucesso se tiver encontrado o usuario
        return {'message': 'The username or password is incorrect.'}, 401 #Codigo HTTP para Unauthorized Se não encontrar ou usuario ou senha.

class UserLogout(Resource):

    @jwt_required() #so pode fazer logout se tiver token de login
    def post(self):
        jwt_id = get_jwt()['jti'] #JWT Token Identifier
        BLOCKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200 # codigo HTTP sucesso

