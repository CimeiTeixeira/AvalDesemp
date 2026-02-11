"""
.. topic:: Modelos (tabelas nos bancos de dados)

    Os modelos são classes que definem a estrutura das tabelas dos bancos de dados.

    Este aplicativo utiliza dois bancos de dados. Um para os dados referentes às demandas e o outro para os dados de
    Acordos e Convênios.

    O banco de dados de notas possui os modelos:

    * escala_desempenho
    * escala_metas_individuais
    * fatores
    * metas_individuais
    * notas
    * pesos
    * AFMI (VIEW)
    * MPAF (VIEW)

    Abaixo seguem os Modelos e respectivos campos.
"""
# models.py
import locale

from project import db

## dados o órgão
class Orgao(db.Model):

    __tablename__ = "orgao"

    id    = db.Column(db.Integer,primary_key=True)
    sigla = db.Column(db.String)
    nome  = db.Column(db.String)
    
    def __init__ (self,sigla,nome):

        self.sigla = sigla
        self.nome = nome

    def __repr__ (self):
        return f"{self.sigla};{self.nome};" 

## Pesos da avaliação final
class Estrutura_AF (db.Model):

    __tablename__ = "estrutura_af"

    id    = db.Column(db.Integer,primary_key=True)
    peso_institucional   = db.Column(db.Float)
    peso_individual = db.Column(db.Float)
    
    def __init__ (self,peso_institucional,peso_individual):

        self.peso_institucional = peso_institucional
        self.peso_individual = peso_individual

    def __repr__ (self):
        return f"{self.peso_institucional};{self.peso_individual};" 

## Pesos da avaliação individual
class Estrutura_AI (db.Model):

    __tablename__ = "estrutura_ai"

    id    = db.Column(db.Integer,primary_key=True)
    peso_metas   = db.Column(db.Float)
    peso_fatores = db.Column(db.Float)
    
    def __init__ (self,peso_metas,peso_fatores):

        self.peso_metas = peso_metas
        self.peso_fatores = peso_fatores

    def __repr__ (self):
        return f"{self.peso_metas};{self.peso_fatores};" 

## escala de desempenho
class Escala_Desempenho (db.Model):

    __tablename__ = "escala_desempenho"

    id            = db.Column(db.Integer,primary_key=True)
    escala        = db.Column(db.String)
    alcance       = db.Column(db.Float)
    intervalo_inf = db.Column(db.Float)
    intervalo_sup = db.Column(db.Float)

    def __init__ (self,escala,alcance,intevalo_inf,intervalo_sup):

        self.escala        = escala
        self.alcance       = alcance
        self.intevalo_inf  = intevalo_inf
        self.intervalo_sup = intervalo_sup

    def __repr__ (self):
        return f"{self.escala};{self.alcance};{self.intevalo_inf};{self.intervalo_sup};"

## escala de metas individuais
class Escala_Metas_Individuais (db.Model):

    __tablename__ = "escala_metas_individuais"

    id          = db.Column(db.Integer,primary_key=True)
    alcance_inf = db.Column(db.Float)
    alcance_sup = db.Column(db.Float)
    pontuacao   = db.Column(db.Float)
    
    def __init__ (self,alcance_inf,alcance_sup,pontuacao):

        self.alcance_inf = alcance_inf
        self.alcance_sup = alcance_sup
        self.pontuacao   = pontuacao

    def __repr__ (self):
        return f"{self.alcance_inf};{self.alcance_sup};{self.pontuacao};"

## fatores
class Fatores (db.Model):

    __tablename__ = "fatores"

    id      = db.Column(db.Integer,primary_key=True)
    apelido = db.Column(db.String)
    desc    = db.Column(db.String)
    peso    = db.Column(db.Float)
    
    def __init__ (self,apelido,desc,peso):

        self.apelido = apelido
        self.desc    = desc
        self.peso    = peso

    def __repr__ (self):
        return f"{self.apelido};{self.desc};{self.peso};"   

## metas_individuais
class Metas_Individuais (db.Model):

    __tablename__ = "metas_individuais"

    id      = db.Column(db.Integer,primary_key=True)
    nome    = db.Column(db.String)
    ano     = db.Column(db.Integer)
    ciclo   = db.Column(db.Integer)
    meta    = db.Column(db.String)
    alcance = db.Column(db.Float)
    peso    = db.Column(db.Float)
    
    def __init__ (self,nome,ano,ciclo,meta,alcance,peso):

        self.nome    = nome
        self.ano     = ano
        self.ciclo   = ciclo
        self.meta    = meta
        self.alcance = alcance
        self.peso    = peso

    def __repr__ (self):
        return f"{self.nome};{self.ano};{self.ciclo};{self.meta};{self.alcance};{self.peso};"
              
## notas    
class Notas (db.Model):

    __tablename__ = "notas"

    id         = db.Column(db.Integer,primary_key=True)
    nome       = db.Column(db.String)
    ano        = db.Column(db.Integer)
    ciclo      = db.Column(db.Integer)
    fator_id   = db.Column(db.Integer)
    nota_chefe = db.Column(db.Float)
    nota_aa    = db.Column(db.Float)
    nota_pares = db.Column(db.Float)
    qtd_pares  = db.Column(db.Integer)
    media_pares= db.Column(db.Float)
    nota_institucional = db.Column(db.Float)
    
    def __init__ (self,nome,ano,ciclo,fator_id,nota_chefe,nota_aa,nota_pares,qtd_pares,media_pares,nota_institucional):

        self.nome       = nome
        self.ano        = ano
        self.ciclo      = ciclo
        self.fator_id   = fator_id
        self.nota_chefe = nota_chefe
        self.nota_aa    = nota_aa
        self.nota_pares = nota_pares
        self.qtd_pares  = qtd_pares
        self.media_pares = media_pares
        self.nota_institucional = nota_institucional

    def __repr__ (self):
        return f"{self.nome};{self.ano};{self.ciclo};{self.fator_id};{self.nota_chefe};{self.nota_aa};{self.nota_pares};{self.qtd_pares};{self.media_pares};{self.nota_institucional};"
## pesos
class Pesos (db.Model):

    __tablename__ = "pesos"

    id    = db.Column(db.Integer,primary_key=True)
    chefe = db.Column(db.Float)
    aa    = db.Column(db.Float)
    pares = db.Column(db.Float)
    
    def __init__ (self,chefe,aa,pares):

        self.chefe = chefe
        self.aa    = aa
        self.pares = pares

    def __repr__ (self):
        return f"{self.chefe};{self.aa};{self.pares};" 

### VIEWS DO BANCO

## contas das metas individuais
class AFMI (db.Model):

    __tablename__ = "afmi"

    chave      = db.Column(db.String,primary_key=True)
    nome       = db.Column(db.String)
    ano        = db.Column(db.Integer)
    ciclo      = db.Column(db.Integer)
    qtd_metas  = db.Column(db.Integer)
    AFMI       = db.Column(db.Float)
    soma_pesos = db.Column(db.Float)
    soma_ap    = db.Column(db.Float)
    
    def __init__ (self,chave,nome,ano,ciclo,qtd_metas,AFMI,soma_pesos,soma_ap):

        self.chave     = chave
        self.nome      = nome
        self.ano       = ano
        self.ciclo     = ciclo
        self.qtd_metas = qtd_metas
        self.AFMI      = AFMI
        self.soma_pesos = soma_pesos
        self.soma_ap   = soma_ap

    def __repr__ (self):
        return f"{self.chave};{self.nome};{self.ano};{self.ciclo};{self.qtd_metas};{self.AFMI};{self.soma_pesos};{self.soma_ap};"

## contas dos fatores
class MPAF (db.Model):

    __tablename__ = "mpaf"

    chave               = db.Column(db.String,primary_key=True)
    nome                = db.Column(db.String)
    ano                 = db.Column(db.Integer)
    ciclo               = db.Column(db.Integer)
    nota_institucional  = db.Column(db.Float)
    qtd_pares           = db.Column(db.Integer)
    soma_fatores_pesos  = db.Column(db.Float)
    soma_notas_chefe    = db.Column(db.Float)
    soma_notas_aa       = db.Column(db.Float)
    soma_notas_pares    = db.Column(db.Float)
    media_notas_pares_vezes_pesos = db.Column(db.Float)
    pontos_chefe        = db.Column(db.Float)
    pontos_aa           = db.Column(db.Float)
    pontos_pares        = db.Column(db.Float)
    soma_pesos          = db.Column(db.Float)
    MPFC                = db.Column(db.Float)
    MPFAA               = db.Column(db.Float)
    MPFP                = db.Column(db.Float)
    total_chefe         = db.Column(db.Float)
    total_aa            = db.Column(db.Float)
    total_pares         = db.Column(db.Float)
    nota_fatores        = db.Column(db.Float)
    nota_fatores_sem_pares = db.Column(db.Float)
    
    def __init__ (self,chave,nome,ano,ciclo,nota_institucional,qtd_pares,soma_fatores_pesos,soma_notas_chefe,soma_notas_aa,
                  soma_notas_pares, media_notas_pares_vezes_pesos, pontos_chefe, 
                  pontos_aa,pontos_pares,MPFC,MPFAA,MPFP,total_chefe,total_aa,    
                  total_pares,nota_fatores,nota_fatores_sem_pares):

        self.chave               = chave
        self.nome                = nome
        self.ano                 = ano
        self.ciclo               = ciclo
        self.nota_institucional  = nota_institucional
        self.qtd_pares           = qtd_pares
        self.soma_fatores_pesos  = soma_fatores_pesos
        self.soma_notas_chefe    = soma_notas_chefe
        self.soma_notas_aa       = soma_notas_aa
        self.soma_notas_pares    = soma_notas_pares
        self.media_notas_pares_vezes_pesos = media_notas_pares_vezes_pesos
        self.pontos_aa           = pontos_aa
        self.pontos_pares        = pontos_pares
        self.MPFC                = MPFC
        self.MPFAA               = MPFAA
        self.MPFP                = MPFP
        self.total_chefe         = total_chefe
        self.total_aa            = total_aa
        self.total_pares         = total_pares
        self.nota_fatores        = nota_fatores
        self.nota_fatores_sem_pares = nota_fatores_sem_pares

    def __repr__ (self):
        return f"{self.chave};{self.nome};{self.ano};{self.ciclo};{self.nota_institucional};{self.qtd_pares};{self.pontos_chefe};{self.pontos_aa};{self.pontos_pares}"         

