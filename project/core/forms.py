"""

.. topic:: **Core (formulários)**

   * Notas_recursos_Form: utilizado para entrar com as notas.

"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FieldList, FormField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask import flash

from project import db

class NotaFatorForm(FlaskForm):
    """Formulário para uma nota de um fator específico"""
    nota_chefe = StringField('Chefia', default=0, render_kw={"placeholder": "0"})
    nota_aa    = StringField('Auto Avaliação', default=0, render_kw={"placeholder": "0"})
    nota_pares = StringField('Pares', default=0, render_kw={"placeholder": "0"})

class NotasFatoresForm(FlaskForm):

    nome      = StringField('Nome: ', validators=[DataRequired(message="Informe um nome!")])
    ano       = IntegerField('Ano: ', validators=[DataRequired(message="Informe o ano!")])
    ciclo     = IntegerField('Ciclo: ', validators=[DataRequired(message="Informe o ciclo!")])
    nota_institucional = StringField('Nota Institucional: ', default=0, validators=[DataRequired(message="Informe a nota institucional!")])
    qtd_pares = IntegerField('Quantidade de pares: ', default = 0)

    submit   = SubmitField('Registrar')

class AlcanceMetasForm(FlaskForm):

    meta_i  = StringField('Meta: ', validators=[DataRequired(message="Informe a descrição da meta!")])
    alcance = StringField('Nota: ', validators=[DataRequired(message="Informe o alcance!")])
    peso    = SelectField('Peso: ', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], validators=[DataRequired(message="Informe o peso!")])
  
    submit   = SubmitField('Registrar')

class EscalaDesempenhoForm(FlaskForm):

    escala        = StringField('Escala: ', validators=[DataRequired(message="Informe a escala!")])
    alcance       = StringField('Pontuação: ', validators=[DataRequired(message="Informe o alcance!")])
    intervalo_inf = StringField('Intervalo Inferior: ', validators=[DataRequired(message="Informe o intervalo inferior!")])
    intervalo_sup = StringField('Intervalo Superior: ', validators=[DataRequired(message="Informe o intervalo superior!")])
  
    submit   = SubmitField('Registrar')

class PesosForm(FlaskForm):

    chefe = StringField('Chefia: ', validators=[DataRequired(message="Informe o peso do chefe!")])
    aa    = StringField('Autoavaliação: ', validators=[DataRequired(message="Informe o peso da autoavaliação!")])
    pares = StringField('Pares ou Subordinados: ', validators=[DataRequired(message="Informe o peso dos pares!")])

    submit   = SubmitField('Salvar')

class EstruturaAIForm(FlaskForm):

    peso_metas   = StringField('Peso Metas: ', validators=[DataRequired(message="Informe o peso das metas!")])
    peso_fatores = StringField('Peso Fatores: ', validators=[DataRequired(message="Informe o peso dos fatores!")])

    submit   = SubmitField('Salvar')

class EstruturaAFForm(FlaskForm):

    peso_institucional = StringField('Peso Institucional: ', validators=[DataRequired(message="Informe o peso institucional!")])
    peso_individual    = StringField('Peso Individual: ', validators=[DataRequired(message="Informe o peso individual!")])

    submit   = SubmitField('Salvar')

class FatoresForm(FlaskForm):

    apelido = StringField('Apelido: ', validators=[DataRequired(message="Informe o apelido!")])
    desc    = TextAreaField('Descrição: ', validators=[DataRequired(message="Informe a descrição!")])
    peso    = StringField('Peso: ', validators=[DataRequired(message="Informe o peso!")])

    submit   = SubmitField('Registrar')

class OrgaoForm(FlaskForm):

    sigla = StringField('Sigla: ', validators=[DataRequired(message="Informe a sigla!")])
    nome  = StringField('Nome: ', validators=[DataRequired(message="Informe o nome!")])

    submit   = SubmitField('Salvar')
