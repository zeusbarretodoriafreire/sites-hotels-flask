from sql_alchemy import banco

# Modelagem do banco de dados 'banco' com os hoteis.
#As configurações de Hotel vao ficar todas aqui agora.

class UserModel(banco.Model): #criando a classe de modelo do Hotel com base no modelo de banco (objeto da classe SQLALchemy())
    #----------INTEGRAÇÃO COM O BANCO DE DADOS-------:
    #significa que essa classe vai ser uma tabela do banco de dados, em que cada atributo da classe vai ser uma coluna do banco
    #determinando o nome da tabela:
    __tablename__ = 'usuarios' # O nome da tabela pro SQLALchemy saber é usuarios.

    #Dentro da tabela 'usuarios' eu defino essas colunas (mas não são Atributos da classe):
    user_id = banco.Column(banco.Integer, primary_key=True) #cada atributo transformado em coluna e o tipo da variavel
    login = banco.Column(banco.String(40)) #definir o limite até 80 caracteres.
    senha = banco.Column(banco.String(40)) 


    #-------------------------------------------------
    #Construtor e Metodos da classe:

    #construtor da classe, Quando instancio a classe eu passo esses atributos.
    def __init__(self, login, senha):
        #definindo agora os Atributos da classe de fato.
        #Note que a gente nao botou pra ele ele receber user_id, pois assim, cada instancia da classe o
        #SQLAlchemy vai incrementar os Inteiros pra cada usuario criado Automaticamente e Infinitamente.
        #Se o objeto da classe existe ele obrigatoriamente precisa ter login, senha e user_id (automatico).
        self.login = login
        self.senha = senha
        

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }
    
    #Vamos Usar um @classmethod pois eu vou me referir a propria classe com cls. Mas nao vou alterar Atributos
    @classmethod
    def find_user(cls, user_id): #função pra verificar se usuario existe e retornar o proprio.
        #uso essa busca rapida pelo id do usuario pra nao buscar pelo login que é mais sensivel.
        #query (consulta) é um metodo da classe banco.model
        usuario = cls.query.filter_by(user_id=user_id).first() # Em SQL: SELECT * FROM usuarios WHERE user_id = $user_id$, first() pega o primeiro
        if usuario:
            return usuario
        return None
    
    @classmethod
    def find_user_by_login(cls, login):
        # checar se existe usuario com o login que vai ser passado
        # faz uma consulta na propria classe (que herda do banco de dados)
        # login=login, o primeiro login é referente ao mapeamento 'login' do sqlalchemy com relação aos atributos 
        usuario = cls.query.filter_by(login=login).first()
        if usuario:
            return usuario
        return None
    
    def save_user(self):
        banco.session.add(self) #vai abrir uma conexão com o banco e salvar o objeto da classe HotelModel na tabela.
        #Ele é inteligente o suficiente pra saber quais sao os argumentos da classe que a gente passou e ele adiciona com base na Seção A.
        banco.session.commit()
    
    def delete_user(self):
        #uma ação que faz o delete do objeto da classe HotelModel.
        banco.session.delete(self)
        banco.session.commit()

        