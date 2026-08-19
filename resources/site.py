from flask_restful import Resource
from models.site import SiteModel

#lembrando que SiteModel nada mais é do que uma tabela no banco de dados.
class Sites(Resource): #classe pra endpoint de busca geral: todos os sites e todos os respectivos hoteis.
    def get(self): #apenas um metodo de consulta do banco 'get'
        return {'sites': [site.json() for site in SiteModel.query.all()]}  #retorna o json pra cada site existente na classe  SiteModel (tabela)            

class Site(Resource): #definindo a classe Site herdada da classe mão resources para uso do flask.
    def get(self, url): #endpoint de get com url do site
        site = SiteModel.find_site(url) #verifica se existe o site (com url) dentro da classe SiteModel
        if site:
            return site.json() #se existir retorna o json do site
        return {'message': 'Site not found.'}, 404 #codigo HTTP 'not found', caso não encontre

    def post(self, url):
        if SiteModel.find_site(url): #verifica na classe se o site com url ja existe
            return {'message': 'The Site "{}" already exists.'.format(url)}, 400 # codigo HTTP Bad request
        site = SiteModel(url) #se nao existe=> Cria. obs: tem que criar o objeto antes de salvar o objeto
        #antes de executar qualquer operação no banco de dados é sempre bom usar try except.
        try:
            site.save_site() #salva o objeto site na tabela 'sites' do banco de dados.
        except:
            return {'message': 'An internal error ocurred trying to create a new site'}
        return site.json() #retorna o json do site.                  

    def delete(self,url):
        
        site = SiteModel.find_site(url) #instancio a classe SiteModel para criar um objeto da classe chamado 'site' se ja existir url
        if site:
            site.delete_site()
            return {'message': "Site deleted."}, 200 #HTTP code for success
        return {'message': 'Site not found.'}, 404 #HTTP code for 'not found'       