from sql_alchemy import banco
#try:
from models.hotel import HotelModel
# Modelagem do banco de dados 'banco' com os hoteis.
#As configurações de Hotel vao ficar todas aqui agora.

class SiteModel(banco.Model): #criando a classe de modelo do Hotel com base no modelo de banco (objeto da classe SQLALchemy())
    #----------INTEGRAÇÃO COM O BANCO DE DADOS-------:
    #significa que essa classe vai ser uma tabela do banco de dados, em que cada atributo da classe vai ser uma coluna do banco
    #determinando o nome da tabela:
    __tablename__ = 'sites' # O nome da tabela pro SQLALchemy saber é hoteis.

    #agora precisamos mapear pra o SQLALchemy que cada atributo da classe SiteModel seja uma coluna da tabela do banco de dados
    #Isso aqui são os ATRIBUTOS da classe (tabela) SiteModel
    #Esse 'site_id' faz o link das duas tabelas SiteModel <-> HotelModel, todo hotel criado com site_id da tabela de sites vai ficar armazenado aqui
    site_id = banco.Column(banco.Integer, primary_key=True) #essa ideia do site_id sendo inteiro é a mesma logica do user_id, ele cria um inteiro autommatico pra cada usuario.
    url = banco.Column(banco.String(80)) #definir o limite até 80 caracteres.
    hoteis = banco.relationship('HotelModel') #lista de objetos (hoteis) de instancias da classe hotel devido ao termo 'relationship'
    #Essa lista 'hoteis' pega os objetos hoteis que estao relacionados com o site_id e coloca na lista.
    #entao os hoteis que precisam ser deletados ja estao nessa lista 'hoteis'
    #-------------------------------------------------
    #Construtor e Metodos da classe:


    def __init__(self, url):
        #definindo os atributos do meu modelo (classe) de hotel
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis':[hotel.json() for hotel in self.hoteis] #retorna uma lista de json pra cada objeto (hotel) da classe HotelModel
            
        }
    
    #Vamos Usar um @classmethod pois eu vou me referir a propria classe com cls. Mas nao vou alterar Atributos
    @classmethod
    def find_site(cls, url): #função pra verificar se site existe e retornar o proprio.
        #query (consulta) é um metodo da classe banco.model
        site = cls.query.filter_by(url=url).first() # Em SQL: SELECT * FROM hoteis WHERE hotel_id = $hotel_id$, first() pega o primeiro
        if site:
            return site
        return None

    @classmethod
    def find_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None
    
    def save_site(self):
        banco.session.add(self) #vai abrir uma conexão com o banco e salvar o objeto da classe SiteModel na tabela.
        #Ele é inteligente o suficiente pra saber quais sao os argumentos da classe que a gente passou e ele adiciona com base na Seção A.
        banco.session.commit()
    
    def delete_site(self):
        #uma ação que faz o delete do objeto da classe HotelModel.
        banco.session.delete(self)
        banco.session.commit()
        #preciso deletar o hotel da tabela hoteis
        #os hoteis que sao vinculados ao site tem o site_id associado na linha do hotel da tabela 'hoteis'
        #ja que na lista 'hoteis' eu ja tenho os objetos hoteis associados ao site basta eu chamar a função
        #que deleta hotel dentro de hotel.models
        #try:
        for hotel in self.hoteis:
            #hotel ja é um objeto da classe HotelModel (linha da tabela hoteis)
            try: 
                hotel.delete_hotel() #Deletar o Hotel da tabela.
                return {'message': 'Hotel Deleted.'}
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'}, 500 #Código HTTP: Internal Server Error
        
        
        


        