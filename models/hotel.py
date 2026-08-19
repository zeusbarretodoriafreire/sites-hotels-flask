from sql_alchemy import banco

# Modelagem do banco de dados 'banco' com os hoteis.
#As configurações de Hotel vao ficar todas aqui agora.

class HotelModel(banco.Model): #criando a classe de modelo do Hotel com base no modelo de banco (objeto da classe SQLALchemy())
    #----------INTEGRAÇÃO COM O BANCO DE DADOS-------:
    #significa que essa classe vai ser uma tabela do banco de dados, em que cada atributo da classe vai ser uma coluna do banco
    #determinando o nome da tabela:
    __tablename__ = 'hoteis' # O nome da tabela pro SQLALchemy saber é hoteis.

    #agora precisamos mapear pra o SQLALchemy que cada atributo da classe HotelModel seja uma coluna da tabela do banco de dados
    #Seção A
    hotel_id = banco.Column(banco.String, primary_key=True) #cada atributo transformado em coluna e o tipo da variavel
    nome = banco.Column(banco.String(80)) #definir o limite até 80 caracteres.
    estrelas = banco.Column(banco.Float(precision=1)) #definindo quantas casas apos a virgula do Float
    diaria = banco.Column(banco.Float(precision=2)) #2 casas apos a virgula
    cidade = banco.Column(banco.String(80)) 
    #A resposta de "Como o site sabe quais são os hoteis dele?":
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id')) #definindo uma nova coluna na tabela hoteis do banco de dados que 
    #na construção de um novo hotel precisa informar um site_id (inteiro) pro hotel -> iformando em qual site esse hotel vai ficar linkado
    #-------------------------------------------------
    #Construtor e Metodos da classe:


    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        #definindo os atributos do meu modelo (classe) de hotel
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id
        }
    
    #Vamos Usar um @classmethod pois eu vou me referir a propria classe com cls. Mas nao vou alterar Atributos
    @classmethod
    def find_hotel(cls, hotel_id): #função pra verificar se hotel existe e retornar o proprio.
        #query (consulta) é um metodo da classe banco.model
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # Em SQL: SELECT * FROM hoteis WHERE hotel_id = $hotel_id$, first() pega o primeiro
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        banco.session.add(self) #vai abrir uma conexão com o banco e salvar o objeto da classe HotelModel na tabela.
        #Ele é inteligente o suficiente pra saber quais sao os argumentos da classe que a gente passou e ele adiciona com base na Seção A.
        banco.session.commit()
    
    def update_hotel(self, nome, estrelas, diaria, cidade):
        #desenpacotar
        #renomear os atributos vindo do kwargs no self (objeto em questao)
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        #uma ação que faz o delete do objeto da classe HotelModel.
        banco.session.delete(self)
        banco.session.commit()

        