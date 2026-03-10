# Avaliação de Desempenho (AvalDesemp)

## Descrição

Sistema de Avaliação de Desempenho é uma aplicação web desenvolvida em Python-Flask que permite gerenciar e acompanhar as avaliações de desempenho de colaboradores em uma organização.

Na pasta Bundle, neste repositório, já um executável pronto para uso e seu respectivo banco de dados. Mantenha-os sempre juntos, dentro de uma mesma pasta.

## Funcionalidades

### Gestão de Estruturas
- **Órgão**: Sigla e Nome do órgão
- **Estrutura AF**: Configuração dos pesos de avaliação (institucional e individual)
- **Estrutura AI**: Configuração dos pesos de avaliação individual (metas e fatores)
- **Pesos**: Definição dos pesos das avaliações (chefe, autoavaliação, pares)
- **Escala de Desempenho**: Definição das escalas de desempenho

### Avaliação de Pessoas
- **Gestão de Pessoas**: Visualização das avaliações de desempenho
- **Notas por Fatores**: Registro e edição de notas atribuídas por chefe, autoavaliação e pares
- **Metas Individuais**: Gestão de metas individuais e seu alcance
- **Espelho de Avaliação**: Visualização consolidada da avaliação de uma pessoa

### Administração
- **Fatores de Avaliação**: Gerenciamento dos fatores utilizados nas avaliações
- **Configuração**: Edição das estruturas e escalas de avaliação

## Requisitos

- Python 3.13.9+
- Flask 3.1.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.36
- WTForms 3.2.1
- Flask-WTF 1.2.2

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual: `venv\Scripts\activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Coloque o arquivo do banco de dados (ver pasta Bundle) no local definido em `instance/flask.cfg`
5. Execute a aplicação: `python app.py`

OU

1. Copie os 2 arquivos da pasta Bundle (executável e banco de dados) para uma pasta local. Nesta modalidade, os arquivos devem estar sempre juntos.
2. Ao executar o arquivo, será montada um ambiente em pasta temporária para execução da aplicação (Pyinstaller).

## Uso

A aplicação é acessível em `http://localhost:5000` após iniciar o servidor Flask.

### Menu de Navegação

- **Início**: Página inicial da aplicação
- **Estrutura AF**: Configuração dos pesos de avaliação (institucional e individual)
- **Estrutura AI**: Configuração dos pesos de avaliação individual (metas e fatores)
- **Pessoas**: Visualização das avaliações de desempenho
- **Escala Desempenho**: Gestão das escalas de desempenho
- **Pesos**: Configuração dos pesos das avaliações
- **Fatores**: Gestão dos fatores de avaliação
- **Sobre**: Informações sobre a aplicação

## Arquitetura

A aplicação utiliza a seguinte estrutura:

```
project/
├── __init__.py           # Inicialização da aplicação
├── models.py             # Definição dos modelos de dados
├── core/
│   ├── __init__.py       # Blueprint do core
│   ├── views.py          # Rotas e lógica de negócio
│   ├── forms.py          # Formulários WTForms
│   └── __pycache__/
├── error_pages/          # Páginas de erro
├── static/               # Arquivos estáticos (CSS, JS, imagens)
└── templates/            # Templates HTML
```

## Banco de Dados

A aplicação utiliza SQLite como banco de dados. O arquivo de banco fica no local definido em `instance/flask.cfg`, ou no diretório da aplicação (PyInstaller).

## Configuração

A configuração da aplicação é feita através do arquivo `instance/flask.cfg` que detecta automaticamente se a aplicação está sendo executada como um bundle PyInstaller.
