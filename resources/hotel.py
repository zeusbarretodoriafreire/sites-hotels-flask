from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required 
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
import sqlite3  

#Esse arquivo é onde eu defino a classe hoteis e o que ela faz. Ela é uma lista de Hoteis

#a biblioteca do flask_restful converte automaticamente o retorno de get(self) para JSON

#definindo os parametros de consulta path (url) OPCIONAIS.
path_params = reqparse.RequestParser() #reqparse é um modulo (arquivo.py), RequestParser é a classe dentro desse modulo. Entao path_params é um objeto da classe agora.
path_params.add_argument('cidade', type=str, location='args') #add_argument é um método já definido da classe RequestParser
path_params.add_argument('estrelas_min', type=float, location='args')
path_params.add_argument('estrelas_max', type=float, location='args')
path_params.add_argument('diaria_min', type=float, location='args')
path_params.add_argument('diaria_max', type=float, location='args')
path_params.add_argument('limit', type=float, location='args')
path_params.add_argument('offset', type=float, location='args')
#se eu não passar um desses argumentos ele vai ficar como None.



class Hoteis(Resource):
    def get(self): #solicitar lista de hoteis do database.
        
        connection = sqlite3.connect('instance/banco.db')
        cursor = connection.cursor()
        
        dados = path_params.parse_args() #recebendo todos os dados de parametros de consulta em 'dados'
        #precisamos pegar apenas os dados que não são None (os que foram passados pelo usuario)
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None} #cria novo dicionario com chave:valor pra cada chave no dicionario dados se o valor for dif de None.
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            consulta = consulta_sem_cidade
            
        else:
            consulta = consulta_com_cidade
            
        tupla = tuple([parametros[chave] for chave in parametros])
        resultado = cursor.execute(consulta, tupla)
        
        #considerando que resultado vai ser a consulta no banco de dados com o filtro do usuario
        #vamos montar o retorno de hoteis de acordo com o filtro de busca do usuario
        hoteis = [] #hoteis é uma lista de dicionarios, cada dicionario um hotel.
        for coluna in resultado: #resultado é como se fosse uma tabela, cada linha seria um hotel existente, cada coluna (linha[0]...) o parametro do hotel
            hoteis.append({
                'hotel_id': coluna[0],
                'nome': coluna[1],
                'estrelas': coluna[2],
                'diaria': coluna[3],
                'cidade': coluna[4],
                'site_id': coluna[5]
            })

        return {'hoteis': hoteis} # retorno um dicionario 
        


#Definindo os Recursos da API: Nada mais é do que requisições que a API faz pro Backend (aqui).
class Hotel(Resource):
    #definindo esses novos Atributos da classe: elementos que eu vou sempre esperar receber do JSON
    atributos = reqparse.RequestParser() #criando um objeto da classe pra pegar os argumentos do JSON que o front enviar
    #Aqui são todos os dados que eu espero receber no JSON: 
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank")
    atributos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank")
    atributos.add_argument('site_id', type=int, required=True, help="Every hotel need to be linked to a site")
   


    def get(self, hotel_id): #get é só solicitar dados pro backend e receber.
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json() #o return ele sempre interrompe a função
        return {'message': 'Hotel not found'} , 404 #Status Code HTTP Not Found
        
    #toda requisição do frontend (usuario) para alteração no database precisa do token de login: @jwt_required  
    @jwt_required() #Antes de fazer um post o frontend precisa enviar o token de acesso.
    def post(self, hotel_id): # Criar novo hotel para lista de hoteis.
        if HotelModel.find_hotel(hotel_id): 
            return {"message": "hotel id '{}' already exists.".format(hotel_id)}, 400 #Bad Request

        dados = Hotel.atributos.parse_args() #armazenando todos os atributos no dicionario dados.
        #Aqui o Hotel que vou receber do front no JSON
        hotel = HotelModel(hotel_id, **dados) #utilizando aqui o **kwargs pra desenpacotar o dicionario Dados.
        #tratamento de erros esperados do codigo Save at DataBase.
        if not SiteModel.find_id(dados.get('site_id')):
            return {'message': "The hotel must be associated to an valid site id"}
        try: 
            hotel.save_hotel() #salva o hotel criado no banco de dados
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Código HTTP: Internal Server Error
        return hotel.json()

    #PUT: atualizar dados.
    @jwt_required()
    def put(self, hotel_id): #se a pessoa está usando o PUT ela quer atualizar os {dados}: atualizar se ja existir hotel_id ou criar novo botel
        dados = Hotel.atributos.parse_args() #armazenando todos os argumentos no dicionario dados.
        hotel = HotelModel.find_hotel(hotel_id) #objeto da classe HotelModel
        if hotel: #se existe eu quero alterar os atributos do objeto da classe HotelModel 
            hotel.update_hotel(**dados) #novo método .update_hotel() pois ele vai precisar atualizar APENAS os {dados}
            hotel.save_hotel() #salvei ele no banco
            return hotel.json(), 200 #codigo de sucesso
        novo_hotel = HotelModel(hotel_id, **dados) #utilizando aqui o **kwargs pra desenpacotar o dicionario Dados.
        #novo_hotel é OBJETO da classe HotelModel. Quando eu instancio a classe ele recebe os atributos definidos no construtor
        try: 
            novo_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 #Código HTTP: Internal Server Error
        return novo_hotel.json(), 201 # codigo HTTP para 'created'.

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try: 
                hotel.delete_hotel() #Deletar o Hotel da tabela.
                return {'message': 'Hotel Deleted.'}
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'}, 500 #Código HTTP: Internal Server Error
        return {'message': 'Hotel not found.'}, 404 # Codigo HTTP pra Not found. retorna mensagem de hotel nao encontrado