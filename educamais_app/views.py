# Arquivo: educamais_app/views.py
from django.shortcuts import render, redirect
from .models import Reeducando
from django.contrib.auth.models import User
from .forms import reeducandoForm, professorForm, cursoForm 
from django.utils import timezone
from datetime import timedelta 

def home(request):
    # Por enquanto vamos renderizar o cadastro na home também, ou uma página temporária
    #1º Busca os contadores reais do banco de dados
    total_reeducandos = Reeducando.objects.count()

    #2º Filtra onde regime_inicial é 1 (Fechado - conform o models.py)
    total_reeducandos_fechado = Reeducando.objects.filter(regime_inicial=1).count()

    #3º Calcula as datas de "Termino próximo (30 dias)"
    # A) Pega a data de hoje + 30 dias
    hoje = timezone.now().date()
    aprox_30_dias = hoje + timedelta(days=30)

    #4º Conta quantos reeducandos têm data_prevista_termino entre hoje e 30 dias
    total_reeducandos_termino_proximo = Reeducando.objects.filter(
        data_prevista_termino__range=[hoje, aprox_30_dias]
    ).count()

    # Cria o dicionario de contexto para enviar ao HTML
    context = {
        'total_reeducandos': total_reeducandos,
        'total_reeducandos_fechado': total_reeducandos_fechado,
        'total_reeducandos_termino_proximo': total_reeducandos_termino_proximo
    }

    return render(request, 'educamais_app/home.html',context) 

def cadastro_aluno(request):
    sucesso = False

    if request.method == 'POST':
        form = reeducandoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = reeducandoForm()
    else:
        form = reeducandoForm()

    return render(request, 'educamais_app/cadastro_aluno.html', {
        'form': form,
        'sucesso': sucesso
    })

def cadastro_professor(request):
    sucesso = False

    if request.method == 'POST':
        form = professorForm(request.POST)
        if form.is_valid():
            #1º Captura os dados mas não salva no banco ainda (commit =False)
            professor = form.save(commit=False)

            #2º Cria o usuário de login do Django (Sistema de Auth)
            # - Usamos o CPF como username para garantir unicidade, ou o email
            username = form.cleaned_data['cpf'].replace('.', '').replace('-', '')
            senha = form.cleaned_data['senha_login']

            #Cria o usuário com segurança (senha criptografada automaticamente)
            novo_usuario = User.objects.create_user(username=username, password=senha)

            #3º Vincula o usuário criado ao professor
            professor.usuario = novo_usuario #Conecta o login ao professor
            professor.save()  # Salva o professor no banco
            
            sucesso = True
            form = professorForm() # Limpa o formulário após o cadastro
    else:
        form = professorForm()

    return render(request, 'educamais_app/cadastro_professor.html', {
        'form': form,
        'sucesso': sucesso
    })

def cadastro_curso(request):
    sucesso = False

    if request.method == 'POST':
        form = cursoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = cursoForm()
    else:
        form = cursoForm()

    return render(request, 'educamais_app/cadastro_curso.html', {
        'form': form,
        'sucesso': sucesso
    })


'''
    sucesso = False
    1º O Estado inicial (A "Página em branco")

       Quando o usuário entra na página pela primeira vez (para preencher o formulário), ele ainda não salvo nada.

       A) Se sucesso começasse como True, a mensagem de sucesso apareceria sem o usuário ter feito nada.
       B) Começando como False, a mensagem só aparece depois que o usuário preenche o formulário e clica em "Salvar". 
       
'''