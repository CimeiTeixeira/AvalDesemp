"""
.. topic:: Core (views)

    Este é o módulo inicial do sistema.

    Apresenta as telas de início.

.. topic:: Calculadora de Notas

    * Tela inicial: index
    * Tela de cedidos: cedidos
    * Tela de recursos: recursos

"""

# core/views.py

from flask import render_template,url_for,flash, redirect, Blueprint, request
from project import db

from project.core.forms import AlcanceMetasForm, NotasFatoresForm, EscalaDesempenhoForm,\
                               PesosForm, EstruturaAIForm, EstruturaAFForm, FatoresForm, OrgaoForm

from project.models import AFMI,MPAF, Escala_Desempenho,\
                           Fatores, Metas_Individuais, Notas, Estrutura_AF, Estrutura_AI, Pesos, Orgao

core = Blueprint("core",__name__)

def virg_ponto(valor):
    if valor == None or valor == '':
            return 0
    else:
        return str(valor).replace(',', '.')
    
def ponto_virg(valor):
    if valor == None or valor == '':
            return 0
    else:
        return str(valor).replace('.', ',')

@core.route('/')
def index():
    """
    +---------------------------------------------------------------------------------------+
    |Apresenta a tela inicial do aplicativo.                                                |
    +---------------------------------------------------------------------------------------+
    """

    peso_original = db.session.query(Pesos).first()

    if not peso_original:
        
        registrar_peso = Pesos(chefe=0.6, aa=0.15, pares=0.25)

        db.session.add(registrar_peso)
        db.session.commit()

    estrutura_original = db.session.query(Estrutura_AI).first()

    if not estrutura_original:

        registrar_estrutura = Estrutura_AI(peso_metas=0.6, peso_fatores=0.4)

        db.session.add(registrar_estrutura)
        db.session.commit()

    estrutura_af_original = db.session.query(Estrutura_AF).first()

    if not estrutura_af_original:

        registrar_estrutura_af = Estrutura_AF(peso_institucional=0.8, peso_individual=0.2)

        db.session.add(registrar_estrutura_af)
        db.session.commit()

    return render_template ('index.html')

@core.route('/sobre')
def sobre():
    """
    +---------------------------------------------------------------------------------------+
    |Exibe o conteúdo do arquivo readme.md da pasta project convertido para HTML.          |
    +---------------------------------------------------------------------------------------+
    """
    import os
    from flask import current_app
    import re
    
    # Obtém o caminho do readme.md na pasta project
    if getattr(current_app, 'frozen', False):
        readme_path = os.path.join(current_app.root_path, 'readme.md')
    else:
        readme_path = os.path.join(current_app.root_path, 'readme.md')
    
    conteudo_html = ""
    if os.path.exists(readme_path):
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Converte o conteúdo para HTML
            linhas = conteudo.split('\n')
            html_parts = []
            em_lista = False
            em_tabela = False
            
            for linha in linhas:
                linha = linha.rstrip()
                
                # Títulos numerados (ex: "1 Estrutura da Avaliação Final")
                if re.match(r'^\d+(\.\d+)* ', linha):
                    if em_lista:
                        html_parts.append('</ul>')
                        em_lista = False
                    if em_tabela:
                        html_parts.append('</tbody></table>')
                        em_tabela = False
                    
                    nivel = len(re.findall(r'\.', linha.split()[0])) + 1
                    # Mantém a numeração no texto
                    html_parts.append(f'<h{min(nivel+1, 6)} class="section-title">{linha}</h{min(nivel+1, 6)}>')
                
                # Itens de lista (começam com • ou são sub-itens com letras)
                elif linha.strip().startswith('•') or re.match(r'^[a-z]\. ', linha.strip()):
                    if em_tabela:
                        html_parts.append('</tbody></table>')
                        em_tabela = False
                    if not em_lista:
                        html_parts.append('<ul class="custom-list">')
                        em_lista = True
                    texto = re.sub(r'^[•a-z]\.? ', '', linha.strip())
                    html_parts.append(f'<li>{texto}</li>')
                
                # Tabelas markdown (linha com |)
                elif '|' in linha and linha.strip():
                    if em_lista:
                        html_parts.append('</ul>')
                        em_lista = False
                    
                    # Ignora linhas separadoras
                    if re.match(r'^\s*\|[:\s-]+\|', linha):
                        continue
                    
                    if not em_tabela:
                        html_parts.append('<table class="table table-bordered table-striped mt-3">')
                        html_parts.append('<tbody>')
                        em_tabela = True
                    
                    colunas = [col.strip() for col in linha.split('|') if col.strip()]
                    if colunas:
                        html_parts.append('<tr>')
                        for col in colunas:
                            html_parts.append(f'<td>{col}</td>')
                        html_parts.append('</tr>')
                
                # Texto em itálico entre asteriscos
                elif linha.strip().startswith('*') and linha.strip().endswith('*'):
                    if em_lista:
                        html_parts.append('</ul>')
                        em_lista = False
                    if em_tabela:
                        html_parts.append('</tbody></table>')
                        em_tabela = False
                    texto = linha.strip().strip('*')
                    html_parts.append(f'<p class="text-muted font-italic">{texto}</p>')
                
                # Linha vazia
                elif not linha.strip():
                    if em_lista:
                        html_parts.append('</ul>')
                        em_lista = False
                    if em_tabela:
                        html_parts.append('</tbody></table>')
                        em_tabela = False
                
                # Texto normal
                else:
                    if linha.strip():
                        if em_lista:
                            html_parts.append('</ul>')
                            em_lista = False
                        if em_tabela:
                            html_parts.append('</tbody></table>')
                            em_tabela = False
                        html_parts.append(f'<p>{linha.strip()}</p>')
            
            # Fecha tags abertas
            if em_lista:
                html_parts.append('</ul>')
            if em_tabela:
                html_parts.append('</tbody></table>')
            
            conteudo_html = '\n'.join(html_parts)
            
        except Exception as e:
            conteudo_html = f"<p class='text-danger'>Erro ao ler o arquivo: {str(e)}</p>"
    else:
        conteudo_html = f"<p class='text-danger'>Arquivo readme.md não encontrado em: {readme_path}</p>"
    
    return render_template('sobre.html', conteudo=conteudo_html)

@core.route('/lista_pessoas', methods=['GET', 'POST'])
def lista_pessoas():
    """
    +---------------------------------------------------------------------------------------+
    |Dados da avaliação de uma pessoa.                                                      |
    +---------------------------------------------------------------------------------------+
    """

    escala_desemp = db.session.query(Escala_Desempenho).order_by(Escala_Desempenho.alcance).all()

    pesos_ai = db.session.query(Estrutura_AI).first()

    pesos_af = db.session.query(Estrutura_AF).first()

    calc = db.session.query(MPAF.nome,
                            MPAF.ano,
                            MPAF.ciclo,
                            MPAF.nota_institucional,
                            AFMI.qtd_metas,
                            AFMI.AFMI,
                            MPAF.qtd_pares,
                            MPAF.MPFAA,
                            MPAF.MPFP,
                            MPAF.MPFC,
                            MPAF.total_chefe,
                            MPAF.total_aa,
                            MPAF.total_pares,
                            MPAF.nota_fatores,
                            MPAF.nota_fatores_sem_pares)\
                     .outerjoin(AFMI, AFMI.chave == MPAF.chave)\
                     .all()  

    pessoas = []

    for indiv in calc:

        pessoa = {}

        pessoa['nome'] = indiv.nome
        pessoa['ano'] = indiv.ano
        pessoa['ciclo'] = indiv.ciclo
        pessoa['nota_institucional'] = round(float(indiv.nota_institucional),2) if indiv.nota_institucional is not None else 0

        if indiv.qtd_metas is None:
            pessoa['qtd_metas'] = 0
        else:    
            pessoa['qtd_metas'] = indiv.qtd_metas

        pessoa['nota_metas'] = round(float(indiv.AFMI),2) if indiv.AFMI is not None else 0

        if indiv.qtd_pares == 0:
            pessoa['nota_fatores'] = round(float(indiv.nota_fatores_sem_pares),2) if indiv.nota_fatores_sem_pares is not None else 0
        else:
            pessoa['nota_fatores'] = round(float(indiv.nota_fatores),2) if indiv.nota_fatores is not None else 0

        # NOTA PARES SEM PESO
        pessoa['nota_pares'] = round(float(indiv.MPFP),2) if indiv.MPFP is not None else 0    
        # NOTA CHEFES SEM PESO
        pessoa['nota_chefe'] = round(float(indiv.MPFC),2) if indiv.MPFC is not None else 0
        # NOTA AUTOAVALIAÇÃO SEM PESO
        pessoa['nota_aa'] = round(float(indiv.MPFAA),2) if indiv.MPFAA is not None else 0

        pessoa['nota_final_individual'] = round((pessoa['nota_metas'] * pesos_ai.peso_metas + pessoa['nota_fatores'] * pesos_ai.peso_fatores) / (pesos_ai.peso_metas + pesos_ai.peso_fatores),2)

        for escala in escala_desemp:

            if pessoa['nota_final_individual'] >= escala.intervalo_inf and pessoa['nota_final_individual'] <= escala.intervalo_sup:
                pessoa['pontuacao_pagamento'] = escala.alcance
                pessoa['nota_final_individual_corrigida'] = escala.intervalo_sup

        pessoa['avaliacao_final'] = round((pessoa['nota_final_individual_corrigida'] * pesos_af.peso_individual + indiv.nota_institucional * pesos_af.peso_institucional) / (pesos_af.peso_individual + pesos_af.peso_institucional),2)

        pessoas.append(pessoa)

   
    return render_template('lista_pessoas.html', pessoas=pessoas)

@core.route('/<int:ano>/<int:ciclo>/<nome>/deleta_pessoa', methods=['GET', 'POST'])
def deleta_pessoa(ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Remove registros da avaliação de uma pessoa.                                           |
    |Recebe o nome da pessoa como parâmetro.                                                |
    +---------------------------------------------------------------------------------------+
    """

    db.session.query(Metas_Individuais).filter(Metas_Individuais.nome == nome,
                                               Metas_Individuais.ano  == ano,
                                               Metas_Individuais.ciclo == ciclo).delete()

    db.session.commit()

    db.session.query(Notas).filter(Notas.nome == nome,
                                   Notas.ano == ano,
                                   Notas.ciclo == ciclo).delete()

    db.session.commit()

    flash('Notas e metas de '+ nome +' foram deletadas.','sucesso')

    return redirect(url_for('core.lista_pessoas'))         

@core.route('/add_notas', methods=['GET', 'POST'])
def add_notas():
    """
    +---------------------------------------------------------------------------------------+
    |Notas atribuidas por chefe, autoavaliação e pares.                                     |
    |Utiliza os fatores existentes na tabela fatores.                                        |
    +---------------------------------------------------------------------------------------+
    """

    form = NotasFatoresForm()
    fatores = db.session.query(Fatores).order_by(Fatores.apelido).all()

    if form.validate_on_submit():
        
        # Processa os dados enviados pelo formulário
        for idx, fator in enumerate(fatores):
            # Recupera os dados dos campos dinâmicos
            nota_chefe_field = f"nota_chefe_{idx}"
            nota_aa_field = f"nota_aa_{idx}"
            nota_pares_field = f"nota_pares_{idx}"
            
            if nota_chefe_field in request.form:
                nota_chefe = request.form.get(nota_chefe_field, 0)
                nota_aa = request.form.get(nota_aa_field, 0)
                nota_pares = request.form.get(nota_pares_field, 0)

                nota_chefe_val = float(virg_ponto(nota_chefe)) if nota_chefe else 0
                nota_aa_val = float(virg_ponto(nota_aa)) if nota_aa else 0
                nota_pares_val = float(virg_ponto(nota_pares)) if nota_pares else 0
                
                # Cria nova nota para este fator
                nova_nota = Notas(
                    nome=form.nome.data,
                    ano=form.ano.data,
                    ciclo=form.ciclo.data,
                    nota_institucional=float(virg_ponto(form.nota_institucional.data)) if form.nota_institucional.data else 0,
                    fator_id=fator.id,
                    nota_chefe=nota_chefe_val,
                    nota_aa=nota_aa_val,
                    nota_pares=nota_pares_val,
                    media_pares=nota_pares_val/form.qtd_pares.data if form.qtd_pares.data > 0 else 0,
                    qtd_pares=form.qtd_pares.data
                )
                db.session.add(nova_nota)
        
        db.session.commit()
        flash(f'Notas de {form.nome.data} foram registradas!', 'sucesso')
        return redirect(url_for('core.add_meta', ano=form.ano.data, ciclo=form.ciclo.data, nome=form.nome.data))

    else:
        return render_template('add_notas_dinamico.html', form=form, fatores=fatores)


@core.route('/<int:ano>/<int:ciclo>/<nome>/see_notas', methods=['GET', 'POST'])
def see_notas(ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Ver/Editar notas atribuidas por chefe, autoavaliação e pares.                          |
    |Utiliza os fatores existentes na tabela fatores.                                        |
    +---------------------------------------------------------------------------------------+
    """

    form = NotasFatoresForm()
    fatores = db.session.query(Fatores).order_by(Fatores.apelido).all()
    notas_fatores = db.session.query(Notas).filter(Notas.nome == nome,
                                                   Notas.ano == ano,
                                                   Notas.ciclo == ciclo).order_by(Notas.fator_id).all()

    if form.validate_on_submit():
        
        # Processa os dados enviados pelo formulário
        for idx, fator in enumerate(fatores):
            # Recupera os dados dos campos dinâmicos
            nota_chefe_field = f"nota_chefe_{idx}"
            nota_aa_field = f"nota_aa_{idx}"
            nota_pares_field = f"nota_pares_{idx}"
            
            if nota_chefe_field in request.form:
                nota_chefe = request.form.get(nota_chefe_field, 0)
                nota_aa = request.form.get(nota_aa_field, 0)
                nota_pares = request.form.get(nota_pares_field, 0)

                nota_chefe_val = float(virg_ponto(nota_chefe)) if nota_chefe else 0
                nota_aa_val = float(virg_ponto(nota_aa)) if nota_aa else 0
                nota_pares_val = float(virg_ponto(nota_pares)) if nota_pares else 0
                
                # Procura se já existe nota para este fator
                nota_existe = None
                if notas_fatores:
                    for n in notas_fatores:
                        if n.fator_id == fator.id:
                            nota_existe = n
                            break
                
                if nota_existe:
                    # Atualiza nota existente
                    nota_existe.nota_chefe = nota_chefe_val
                    nota_existe.nota_aa = nota_aa_val
                    nota_existe.nota_pares = nota_pares_val
                    nota_existe.qtd_pares = form.qtd_pares.data
                    nota_existe.nota_institucional = float(virg_ponto(form.nota_institucional.data)) if form.nota_institucional.data else 0
                    nota_existe.media_pares = nota_pares_val/form.qtd_pares.data if form.qtd_pares.data > 0 else 0
                else:
                    # Cria nova nota
                    nova_nota = Notas(
                        nome=form.nome.data,
                        ano=form.ano.data,
                        ciclo=form.ciclo.data,
                        fator_id=fator.id,
                        nota_chefe=nota_chefe_val,
                        nota_aa=nota_aa_val,
                        nota_pares=nota_pares_val,
                        media_pares=nota_pares_val/form.qtd_pares.data if form.qtd_pares.data > 0 else 0,
                        nota_institucional=float(virg_ponto(form.nota_institucional.data)) if form.nota_institucional.data else 0,
                        qtd_pares=form.qtd_pares.data
                    )
                    db.session.add(nova_nota)
        
        db.session.commit()
        flash(f'Notas de {form.nome.data} foram atualizadas!', 'sucesso')
        return redirect(url_for('core.see_notas', ano=form.ano.data, ciclo=form.ciclo.data, nome=form.nome.data))

    else:
        # Preenche o formulário com dados existentes (GET)
        if notas_fatores:
            form.nome.data = notas_fatores[0].nome
            form.ano.data = notas_fatores[0].ano
            form.ciclo.data = notas_fatores[0].ciclo
            form.nota_institucional.data = ponto_virg(str(notas_fatores[0].nota_institucional))
            form.qtd_pares.data = notas_fatores[0].qtd_pares
        
        return render_template('see_notas_dinamico.html', form=form, fatores=fatores, 
                             notas_fatores=notas_fatores, nome=nome, ano=ano, ciclo=ciclo)


@core.route('/<int:ano>/<int:ciclo>/<nome>/lista_metas', methods=['GET', 'POST'])
def lista_metas(ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Lista metas de uma pessoa.                                                             |
    +---------------------------------------------------------------------------------------+
    """
    
    metas = db.session.query(Metas_Individuais).filter(Metas_Individuais.nome == nome,
                                                       Metas_Individuais.ano  == ano,
                                                       Metas_Individuais.ciclo == ciclo).all()

    if metas is not None:

        return render_template('lista_metas.html',nome=nome,ano=ano,ciclo=ciclo,metas=metas)

    else:

        return redirect (url_for('core.add_meta', ano=ano,ciclo=ciclo,nome=nome))


@core.route('/<int:ano>/<int:ciclo>/<nome>/add_meta', methods=['GET', 'POST'])
def add_meta(ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Adicionar meta de uma pessoa.                                                          |
    +---------------------------------------------------------------------------------------+
    """

    def is_float(s):
        """
        Verifica se string pode ser convertida para float.
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    form = AlcanceMetasForm()

    if form.validate_on_submit():

        if not is_float(form.alcance.data):
            flash('A nota deve ser um valor numérico!','erro')
            return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)

        if float(form.alcance.data) < 0 or float(form.alcance.data) > 100:
            flash('A nota deve estar entre 0 e 100!','erro')
            return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)

        ins_meta = Metas_Individuais(ano = ano,
                                     ciclo = ciclo,
                                     nome = nome,
                                     meta = form.meta_i.data,
                                     alcance = form.alcance.data,
                                     peso = form.peso.data)

        db.session.add(ins_meta)

        db.session.commit()

        return redirect(url_for('core.lista_metas',ano=ano,ciclo=ciclo, nome=nome))  

    else:

        return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)  


@core.route('/<int:id>/<int:ano>/<int:ciclo>/<nome>/edit_meta', methods=['GET', 'POST'])
def edit_meta(id,ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Editar meta de uma pessoa.                                                            |
    +---------------------------------------------------------------------------------------+
    """

    def is_float(s):
        """
        Verifica se string pode ser convertida para float.
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    meta = db.session.query(Metas_Individuais).get_or_404(id)
    form = AlcanceMetasForm()

    if form.validate_on_submit():

        if not is_float(virg_ponto(form.alcance.data)):
            flash('A nota deve ser um valor numérico!','erro')
            return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)

        if float(virg_ponto(form.alcance.data)) < 0 or float(virg_ponto(form.alcance.data)) > 100:
            flash('A nota deve estar entre 0 e 100!','erro')
            return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)

        meta.meta = form.meta_i.data
        meta.alcance = float(virg_ponto(form.alcance.data))
        meta.peso = form.peso.data

        db.session.commit()

        flash('Meta atualizada com sucesso!','sucesso')
        return redirect(url_for('core.lista_metas',ano=ano,ciclo=ciclo, nome=nome))

    elif request.method == 'GET':
        form.meta_i.data = meta.meta
        form.alcance.data = ponto_virg(str(meta.alcance))
        form.peso.data = str(int(meta.peso))

    return render_template('add_meta.html',nome=nome,ano=ano,ciclo=ciclo,form=form)


@core.route('/<int:id>/<int:ano>/<int:ciclo>/<nome>/deleta_meta', methods=['GET', 'POST'])
def deleta_meta(id,ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Deleta meta de uma pessoa.                                                             |
    +---------------------------------------------------------------------------------------+
    """    

    db.session.query(Metas_Individuais).filter(Metas_Individuais.id == id).delete()

    db.session.commit()

    flash('Meta deletada!','sucesso')

    return redirect(url_for('core.lista_metas',ano=ano,ciclo=ciclo, nome=nome))  

@core.route('/<int:ano>/<int:ciclo>/<nome>/espelho')
def espelho(ano,ciclo,nome):
    """
    +---------------------------------------------------------------------------------------+
    |Mostra espelho da avaliação de uma pessoa.                                             |
    +---------------------------------------------------------------------------------------+
    """

    orgao = db.session.query(Orgao).first()

    escala_desemp = db.session.query(Escala_Desempenho).order_by(Escala_Desempenho.alcance).all()

    pesos = db.session.query(Pesos).first()

    pesos_ai = db.session.query(Estrutura_AI).first()

    pesos_af = db.session.query(Estrutura_AF).first()

    metas = db.session.query(Metas_Individuais).filter(Metas_Individuais.nome == nome,
                                                       Metas_Individuais.ano  == ano,
                                                       Metas_Individuais.ciclo == ciclo).all()

    notas_fatores = db.session.query(Notas.nota_chefe,
                                     Notas.nota_aa,
                                     Notas.nota_pares,
                                     Fatores.desc,
                                     Fatores.peso)\
                              .filter(Notas.nome == nome,
                                      Notas.ano == ano,
                                      Notas.ciclo == ciclo)\
                              .join(Fatores,Fatores.id == Notas.fator_id)\
                              .order_by(Fatores.apelido)\
                              .all() 

    calc = db.session.query(MPAF.nome,
                            MPAF.ano,
                            MPAF.ciclo,
                            MPAF.nota_institucional,
                            AFMI.qtd_metas,
                            AFMI.AFMI,
                            AFMI.soma_pesos,
                            AFMI.soma_ap,
                            MPAF.qtd_pares,
                            MPAF.soma_fatores_pesos,
                            MPAF.pontos_chefe,
                            MPAF.pontos_aa,
                            MPAF.pontos_pares,
                            MPAF.soma_notas_chefe,
                            MPAF.soma_notas_aa,
                            MPAF.soma_notas_pares,
                            MPAF.MPFC,
                            MPAF.MPFAA,
                            MPAF.MPFP,
                            MPAF.total_chefe,
                            MPAF.total_aa,
                            MPAF.total_pares,
                            MPAF.media_notas_pares_vezes_pesos,
                            MPAF.nota_fatores,
                            MPAF.nota_fatores_sem_pares)\
                     .outerjoin(AFMI, AFMI.chave == MPAF.chave)\
                     .filter(MPAF.nome == nome,
                             MPAF.ano  == ano,
                             MPAF.ciclo == ciclo)\
                     .first()


    nota_metas = round(float(calc.AFMI),2) if calc.AFMI is not None else 0

    if calc.qtd_pares == 0:
        MPAF_indiv = calc.nota_fatores_sem_pares
        peso_chefe = round(float(pesos.chefe + pesos.pares / 2),2)
        peso_aa = round(float(pesos.aa + pesos.pares / 2),2)
        peso_pares = round(float(0),2)
        nota_chefe_final = (calc.pontos_chefe / calc.soma_fatores_pesos) * peso_chefe
        nota_aa_final = (calc.pontos_aa / calc.soma_fatores_pesos) * peso_aa
        nota_pares_final = (calc.media_notas_pares_vezes_pesos / calc.soma_fatores_pesos) * peso_pares
    else:
        MPAF_indiv = calc.nota_fatores
        peso_chefe = round(float(pesos.chefe),2)
        peso_aa = round(float(pesos.aa),2)
        peso_pares = round(float(pesos.pares),2)
        nota_chefe_final = calc.total_chefe
        nota_aa_final = calc.total_aa
        nota_pares_final = calc.total_pares

    nota_final_individual = round((nota_metas * pesos_ai.peso_metas + MPAF_indiv * pesos_ai.peso_fatores) / (pesos_ai.peso_metas + pesos_ai.peso_fatores),2)

    nota_fatores = nota_final_individual

    for escala in escala_desemp:

        if MPAF_indiv >= escala.intervalo_inf and MPAF_indiv <= escala.intervalo_sup:
           alcance = escala.alcance
           conceito = escala.escala
           nota_final_individual_corrigida = escala.intervalo_sup

    avaliacao_final = round((nota_final_individual_corrigida * pesos_af.peso_individual + calc.nota_institucional * pesos_af.peso_institucional) / (pesos_af.peso_individual + pesos_af.peso_institucional),2)

    nota_final = avaliacao_final

    return render_template('espelho.html',metas=metas,notas_fatores=notas_fatores,calc=calc,nome=nome,ciclo=ciclo,
                                          conceito=conceito, alcance=alcance, nota_fatores=nota_fatores, nota_final=nota_final,
                                          nota_final_individual_corrigida = nota_final_individual_corrigida,
                                          peso_chefe = peso_chefe, peso_aa = peso_aa, peso_pares = peso_pares,
                                          nota_chefe_final = nota_chefe_final, nota_aa_final = nota_aa_final, nota_pares_final = nota_pares_final,
                                          orgao = orgao)


# ========== CRUD Escala de Desempenho ==========

@core.route('/lista_escala_desempenho')
def lista_escala_desempenho():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela escala_desempenho.                                  |
    +---------------------------------------------------------------------------------------+
    """
    escalas = db.session.query(Escala_Desempenho).order_by(Escala_Desempenho.alcance).all()
    
    return render_template('lista_escala_desempenho.html', escalas=escalas)


@core.route('/add_escala_desempenho', methods=['GET', 'POST'])
def add_escala_desempenho():
    """
    +---------------------------------------------------------------------------------------+
    |Adiciona um novo registro na tabela escala_desempenho.                                 |
    +---------------------------------------------------------------------------------------+
    """
    form = EscalaDesempenhoForm()
    
    if form.validate_on_submit():
        
        nova_escala = Escala_Desempenho(
            escala        = form.escala.data,
            alcance       = float(form.alcance.data),
            intevalo_inf  = float(form.intervalo_inf.data),
            intervalo_sup = float(form.intervalo_sup.data)
        )
        
        db.session.add(nova_escala)
        db.session.commit()
        
        flash('Escala de desempenho adicionada com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_escala_desempenho'))
    
    return render_template('escala_desempenho_form.html', form=form, acao='Adicionar')


@core.route('/edit_escala_desempenho/<int:escala_id>', methods=['GET', 'POST'])
def edit_escala_desempenho(escala_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela escala_desempenho.                                         |
    +---------------------------------------------------------------------------------------+
    """
    escala = db.session.query(Escala_Desempenho).get_or_404(escala_id)
    
    form = EscalaDesempenhoForm()
    
    if form.validate_on_submit():
        
        escala.escala        = form.escala.data
        escala.alcance       = float(virg_ponto(form.alcance.data))
        escala.intervalo_inf = float(virg_ponto(form.intervalo_inf.data))
        escala.intervalo_sup = float(virg_ponto(form.intervalo_sup.data))
        
        db.session.commit()
        
        flash('Escala de desempenho atualizada com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_escala_desempenho'))
    
    # Preenche o formulário com os dados atuais
    elif request.method == 'GET':
        form.escala.data        = escala.escala
        form.alcance.data       = ponto_virg(str(escala.alcance))
        form.intervalo_inf.data = ponto_virg(str(escala.intervalo_inf))
        form.intervalo_sup.data = ponto_virg(str(escala.intervalo_sup))
    
    return render_template('escala_desempenho_form.html', form=form, acao='Editar')


@core.route('/delete_escala_desempenho/<int:escala_id>')
def delete_escala_desempenho(escala_id):
    """
    +---------------------------------------------------------------------------------------+
    |Deleta um registro da tabela escala_desempenho.                                        |
    +---------------------------------------------------------------------------------------+
    """
    escala = db.session.query(Escala_Desempenho).get_or_404(escala_id)
    
    db.session.delete(escala)
    db.session.commit()
    
    flash('Escala de desempenho deletada com sucesso!', 'sucesso')
    return redirect(url_for('core.lista_escala_desempenho'))


# ========== CRUD Pesos ==========

@core.route('/lista_pesos')
def lista_pesos():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela pesos.                                              |
    +---------------------------------------------------------------------------------------+
    """
    pesos = db.session.query(Pesos).order_by(Pesos.id).all()

    return render_template('lista_pesos.html', pesos=pesos)


@core.route('/edit_pesos/<int:peso_id>', methods=['GET', 'POST'])
def edit_pesos(peso_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela pesos.                                                     |
    +---------------------------------------------------------------------------------------+
    """
    peso = db.session.query(Pesos).get_or_404(peso_id)

    form = PesosForm()

    if form.validate_on_submit():
        peso.chefe = float(virg_ponto(form.chefe.data))
        peso.aa    = float(virg_ponto(form.aa.data))
        peso.pares = float(virg_ponto(form.pares.data))

        db.session.commit()

        flash('Pesos atualizados com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_pesos'))

    elif request.method == 'GET':
        form.chefe.data = ponto_virg(str(peso.chefe))
        form.aa.data    = ponto_virg(str(peso.aa))
        form.pares.data = ponto_virg(str(peso.pares))

    return render_template('pesos_form.html', form=form, acao='Editar')


# ========== Edição Estrutura AF ==========

@core.route('/lista_estrutura_af')
def lista_estrutura_af():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela estrutura_af.                                       |
    +---------------------------------------------------------------------------------------+
    """
    estrutura = db.session.query(Estrutura_AF).order_by(Estrutura_AF.id).first()

    return render_template('lista_estrutura_af.html', estrutura=estrutura)


@core.route('/edit_estrutura_af/<int:estrutura_id>', methods=['GET', 'POST'])
def edit_estrutura_af(estrutura_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela estrutura_af.                                              |
    +---------------------------------------------------------------------------------------+
    """
    estrutura = db.session.query(Estrutura_AF).get_or_404(estrutura_id)

    form = EstruturaAFForm()

    if form.validate_on_submit():
        estrutura.peso_institucional = float(virg_ponto(form.peso_institucional.data))
        estrutura.peso_individual = float(virg_ponto(form.peso_individual.data))

        db.session.commit()

        flash('Estrutura AF atualizada com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_estrutura_af'))

    elif request.method == 'GET':
        form.peso_institucional.data = ponto_virg(str(estrutura.peso_institucional))
        form.peso_individual.data = ponto_virg(str(estrutura.peso_individual))

    return render_template('estrutura_af_form.html', form=form, acao='Editar')


# ========== Edição Estrutura AI ==========

@core.route('/lista_estrutura_ai')
def lista_estrutura_ai():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela estrutura_ai.                                       |
    +---------------------------------------------------------------------------------------+
    """
    estrutura = db.session.query(Estrutura_AI).order_by(Estrutura_AI.id).first()

    return render_template('lista_estrutura_ai.html', estrutura=estrutura)


@core.route('/edit_estrutura_ai/<int:estrutura_id>', methods=['GET', 'POST'])
def edit_estrutura_ai(estrutura_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela estrutura_ai.                                              |
    +---------------------------------------------------------------------------------------+
    """
    estrutura = db.session.query(Estrutura_AI).get_or_404(estrutura_id)

    form = EstruturaAIForm()

    if form.validate_on_submit():
        estrutura.peso_metas = float(virg_ponto(form.peso_metas.data))
        estrutura.peso_fatores = float(virg_ponto(form.peso_fatores.data))

        db.session.commit()

        flash('Estrutura AI atualizada com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_estrutura_ai'))

    elif request.method == 'GET':
        form.peso_metas.data = ponto_virg(str(estrutura.peso_metas))
        form.peso_fatores.data = ponto_virg(str(estrutura.peso_fatores))

    return render_template('estrutura_ai_form.html', form=form, acao='Editar')


# ========== CRUD Fatores ==========

@core.route('/lista_fatores')
def lista_fatores():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela fatores.                                            |
    +---------------------------------------------------------------------------------------+
    """
    fatores = db.session.query(Fatores).order_by(Fatores.apelido).all()

    return render_template('lista_fatores.html', fatores=fatores)


@core.route('/add_fatores', methods=['GET', 'POST'])
def add_fatores():
    """
    +---------------------------------------------------------------------------------------+
    |Adiciona um novo registro na tabela fatores.                                           |
    +---------------------------------------------------------------------------------------+
    """
    form = FatoresForm()

    if form.validate_on_submit():
        novo_fator = Fatores(
            apelido=form.apelido.data,
            desc=form.desc.data,
            peso=float(form.peso.data)
        )

        db.session.add(novo_fator)
        db.session.commit()

        flash('Fator adicionado com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_fatores'))

    return render_template('fatores_form.html', form=form, acao='Adicionar')


@core.route('/edit_fatores/<int:fator_id>', methods=['GET', 'POST'])
def edit_fatores(fator_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela fatores.                                                   |
    +---------------------------------------------------------------------------------------+
    """
    fator = db.session.query(Fatores).get_or_404(fator_id)

    form = FatoresForm()

    if form.validate_on_submit():
        fator.apelido = form.apelido.data
        fator.desc    = form.desc.data
        fator.peso    = float(virg_ponto(form.peso.data))

        db.session.commit()

        flash('Fator atualizado com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_fatores'))

    elif request.method == 'GET':
        form.apelido.data = fator.apelido
        form.desc.data    = fator.desc
        form.peso.data    = ponto_virg(str(fator.peso))

    return render_template('fatores_form.html', form=form, acao='Editar')


@core.route('/delete_fatores/<int:fator_id>')
def delete_fatores(fator_id):
    """
    +---------------------------------------------------------------------------------------+
    |Deleta um registro da tabela fatores.                                                  |
    +---------------------------------------------------------------------------------------+
    """
    fator = db.session.query(Fatores).get_or_404(fator_id)

    db.session.delete(fator)
    db.session.commit()

    flash('Fator deletado com sucesso!', 'sucesso')
    return redirect(url_for('core.lista_fatores'))



# ========== Listagem e Edição de Órgão ==========

@core.route('/lista_orgao')
def lista_orgao():
    """
    +---------------------------------------------------------------------------------------+
    |Lista todos os registros da tabela orgao.                                              |
    +---------------------------------------------------------------------------------------+
    """
    orgao = db.session.query(Orgao).first()
  
    if not orgao:
        return redirect(url_for('core.add_orgao'))

    return render_template('lista_orgao.html', orgao=orgao)


@core.route('/add_orgao', methods=['GET', 'POST'])
def add_orgao():
    """
    +---------------------------------------------------------------------------------------+
    |Adiciona um registro na tabela orgao.                                                  |
    +---------------------------------------------------------------------------------------+
    """
    form = OrgaoForm()

    if form.validate_on_submit():
        orgao = Orgao(sigla=form.sigla.data, nome=form.nome.data)

        db.session.add(orgao)
        db.session.commit()

        flash('Orgao cadastrado com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_orgao'))

    return render_template('orgao_form.html', form=form, acao='Adicionar')


@core.route('/edit_orgao/<int:orgao_id>', methods=['GET', 'POST'])
def edit_orgao(orgao_id):
    """
    +---------------------------------------------------------------------------------------+
    |Edita um registro da tabela orgao.                                                     |
    +---------------------------------------------------------------------------------------+
    """
    orgao = db.session.query(Orgao).get_or_404(orgao_id)

    form = OrgaoForm()

    if form.validate_on_submit():
        orgao.sigla = form.sigla.data
        orgao.nome = form.nome.data

        db.session.commit()

        flash('Órgão atualizado com sucesso!', 'sucesso')
        return redirect(url_for('core.lista_orgao'))

    elif request.method == 'GET':
        form.sigla.data = orgao.sigla
        form.nome.data = orgao.nome

    return render_template('orgao_form.html', form=form, acao='Editar')

