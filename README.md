# 🏨 API REST de Hoteis

API REST desenvolvida com Flask para gerenciamento de hoteis, sites de reservas e usuarios. A aplicacao utiliza SQLite para persistencia dos dados e JWT para proteger operacoes que alteram os recursos.

## 🛠️ Tecnologias

- Python 3
- Flask 3.0.3
- Flask-RESTful 0.3.10
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- SQLite

## 📁 Estrutura do projeto

```text
.
|-- app.py                 # Inicializacao da aplicacao e registro das rotas
|-- blocklist.py           # Tokens JWT invalidados durante o logout
|-- sql_alchemy.py         # Instancia do SQLAlchemy
|-- models/                # Modelos de usuario, site e hotel
|-- resources/             # Recursos e endpoints da API
|-- instance/              # Banco SQLite gerado localmente
|-- requirements.txt       # Dependencias do projeto
```

## 🚀 Como executar

1. Clone o repositorio e acesse a pasta do projeto.
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   ```

   No Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Instale as dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a API:

   ```bash
   python app.py
   ```

A API ficara disponivel em `http://127.0.0.1:5000`. O arquivo `instance/banco.db` e criado automaticamente quando a aplicacao recebe uma requisicao.

## 🔐 Autenticacao

O cadastro e o login usam `login` e `senha` no corpo JSON. O login retorna um token JWT, que deve ser enviado nas operacoes protegidas:

```http
Authorization: Bearer <access_token>
```

### 👤 Cadastrar usuario

```bash
curl -X POST http://127.0.0.1:5000/cadastro \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123456"}'
```

### 🔑 Fazer login

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"login":"admin","senha":"123456"}'
```

A resposta contem o campo `access_token`.

### 🚪 Fazer logout

```bash
curl -X POST http://127.0.0.1:5000/logout \
  -H "Authorization: Bearer <access_token>"
```

O token usado no logout e colocado em uma blocklist em memoria.

## 🔗 Endpoints

### 🏨 Hoteis

| Metodo | Rota | Autenticacao | Descricao |
|---|---|---|---|
| GET | `/hoteis` | Nao | Lista hoteis com filtros opcionais |
| GET | `/hoteis/<hotel_id>` | Nao | Consulta um hotel |
| POST | `/hoteis/<hotel_id>` | Sim | Cadastra um hotel |
| PUT | `/hoteis/<hotel_id>` | Sim | Atualiza ou cria um hotel |
| DELETE | `/hoteis/<hotel_id>` | Sim | Remove um hotel |

Para criar ou atualizar um hotel, envie:

```json
{
  "nome": "Hotel Central",
  "estrelas": 4,
  "diaria": 250.0,
  "cidade": "Sao Paulo",
  "site_id": 1
}
```

O `site_id` deve existir antes do cadastro do hotel. Exemplo de criacao:

```bash
curl -X POST http://127.0.0.1:5000/hoteis/hotel-central \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"nome":"Hotel Central","estrelas":4,"diaria":250.0,"cidade":"Sao Paulo","site_id":1}'
```

Filtros disponiveis em `GET /hoteis`:

- `cidade`
- `estrelas_min` e `estrelas_max`
- `diaria_min` e `diaria_max`
- `limit` e `offset`

Exemplo:

```text
GET /hoteis?cidade=Sao%20Paulo&estrelas_min=3&diaria_max=500&limit=10
```

### 🌐 Sites

| Metodo | Rota | Autenticacao | Descricao |
|---|---|---|---|
| GET | `/sites` | Nao | Lista sites com seus hoteis |
| GET | `/sites/<url>` | Nao | Consulta um site pela URL |
| POST | `/sites/<url>` | Nao | Cadastra um site |
| DELETE | `/sites/<url>` | Nao | Remove um site e seus hoteis relacionados |

Exemplo:

```bash
curl -X POST http://127.0.0.1:5000/sites/exemplo.com
curl http://127.0.0.1:5000/sites
```

### 👤 Usuarios

| Metodo | Rota | Autenticacao | Descricao |
|---|---|---|---|
| GET | `/usuarios/<user_id>` | Nao | Consulta um usuario |
| DELETE | `/usuarios/<user_id>` | Sim | Remove um usuario |
| POST | `/cadastro` | Nao | Cadastra um usuario |
| POST | `/login` | Nao | Gera um token JWT |
| POST | `/logout` | Sim | Invalida o token atual |

## 🗄️ Banco de dados

A aplicacao usa SQLite com SQLAlchemy. As tabelas sao criadas automaticamente no primeiro request:

- `usuarios`
- `sites`
- `hoteis`

## 📝 Observacoes

- O banco local fica em `instance/banco.db`.
- O modo `debug` do Flask esta habilitado ao executar `python app.py`.
- A blocklist de tokens existe apenas em memoria e é perdida quando a aplicacao reinicia.
- Este projeto nao possui uma suite de testes automatizados configurada no momento.
