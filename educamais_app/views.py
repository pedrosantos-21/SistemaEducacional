# Arquivo: educamais_app/views.py
from django.shortcuts import render, redirect
from .models import Reeducando, Matricula, ConteudoHome
from django.contrib.auth.models import User
from .forms import ProfessorForm, ReeducandoForm, CursoForm, MatriculaForm, ProgressoForm, ConteudoHomeForm
from django.utils import timezone
from datetime import timedelta 


# Adicione Progresso nas importações
from .models import Reeducando, ConteudoHome, Progresso 

def home(request):
    # ... (Lógica dos contadores continua igual) ...
    total_reeducandos = Reeducando.objects.count()
    total_reeducandos_fechado = Reeducando.objects.filter(regime_inicial=1).count()
    
    # ... (Lógica de datas continua igual) ...
    hoje = timezone.now().date()
    aprox_30_dias = hoje + timedelta(days=30)
    total_reeducandos_termino_proximo = Reeducando.objects.filter(
        data_prevista_termino__range=[hoje, aprox_30_dias]
    ).count()

    # Configuração da Home
    conteudo, created = ConteudoHome.objects.get_or_create(id=1)

    # --- NOVA LÓGICA: Buscar as 5 últimas atividades ---
    atividades_recentes = Progresso.objects.select_related('matricula__aluno').order_by('-data_conclusao')[:5]

    context = {
        'total_reeducandos': total_reeducandos,
        'total_reeducandos_fechado': total_reeducandos_fechado,
        'total_reeducandos_termino_proximo': total_reeducandos_termino_proximo,
        'conteudo': conteudo,
        'atividades_recentes': atividades_recentes, # <--- Mandando para o HTML
    }

    return render(request, 'educamais_app/home.html', context)

'''


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

'''
def cadastro_aluno(request):
    sucesso = False

    if request.method == 'POST':
        form = ReeducandoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = ReeducandoForm()
    else:
        form = ReeducandoForm()

    return render(request, 'educamais_app/cadastro_aluno.html', {
        'form': form,
        'sucesso': sucesso
    })

def cadastro_professor(request):
    sucesso = False

    if request.method == 'POST':
        form = ProfessorForm(request.POST)
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
            form = ProfessorForm() # Limpa o formulário após o cadastro
    else:
        form = ProfessorForm()

    return render(request, 'educamais_app/cadastro_professor.html', {
        'form': form,
        'sucesso': sucesso
    })

def cadastro_curso(request):
    sucesso = False

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = CursoForm()
    else:
        form = CursoForm()

    return render(request, 'educamais_app/cadastro_curso.html', {
        'form': form,
        'sucesso': sucesso
    })


def cadastro_matricula(request):
    sucesso = False
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = MatriculaForm() # Limpa o formulário
    else:
        form = MatriculaForm()

    return render(request, 'educamais_app/cadastro_matricula.html', {
        'form': form,
        'sucesso': sucesso
    })


def lancamento_nota(request):
    sucesso = False
    if request.method == 'POST':
        form = ProgressoForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = ProgressoForm() # Limpa após salvar
    else:
        form = ProgressoForm()

    return render(request, 'educamais_app/lancamento_nota.html', {
        'form': form,
        'sucesso': sucesso
    })

# ... imports ...

def painel_relatorios(request):
    # Vamos buscar todas as matrículas para listar no relatório geral
    # O select_related ajuda a performance trazendo dados do Aluno e Curso juntos
    relatorios = Matricula.objects.select_related('aluno', 'curso').all()

    # Se o usuário filtrar pelo GET (ex: ?busca=Joao)
    busca = request.GET.get('busca')
    if busca:
        relatorios = relatorios.filter(aluno__nome_completo__icontains=busca)

    return render(request, 'educamais_app/painel_relatorios.html', {
        'relatorios': relatorios
    })

# Importe os novos forms
from .forms import (
    ReeducandoForm, ProfessorForm, CursoForm, MatriculaForm, 
    ProgressoForm, AdministradorForm, GestorForm
)

# ... (Outras views) ...

def cadastro_administrador(request):
    sucesso = False
    if request.method == 'POST':
        form = AdministradorForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            # Cria Usuário do Django
            username = form.cleaned_data['email']
            senha = form.cleaned_data['senha_login']
            novo_usuario = User.objects.create_user(username=username, password=senha)
            
            # Vincula e Salva
            admin_user.usuario = novo_usuario
            admin_user.save()
            
            sucesso = True
            form = AdministradorForm()
    else:
        form = AdministradorForm()

    return render(request, 'educamais_app/cadastro_administrador.html', {
        'form': form,
        'sucesso': sucesso
    })

def cadastro_gestor(request):
    sucesso = False
    if request.method == 'POST':
        form = GestorForm(request.POST)
        if form.is_valid():
            gestor_user = form.save(commit=False)
            # Cria Usuário do Django
            username = form.cleaned_data['email']
            senha = form.cleaned_data['senha_login']
            novo_usuario = User.objects.create_user(username=username, password=senha)
            
            # Vincula e Salva
            gestor_user.usuario = novo_usuario
            gestor_user.save()
            
            sucesso = True
            form = GestorForm()
    else:
        form = GestorForm()

    return render(request, 'educamais_app/cadastro_gestor.html', {
        'form': form,
        'sucesso': sucesso
    })


def gerenciar_home(request):
    # O Segredo: Pega sempre o ID=1. Se não existir, cria vazio.
    conteudo, created = ConteudoHome.objects.get_or_create(id=1)
    
    sucesso = False
    
    if request.method == 'POST':
        # Passamos a 'instance=conteudo' para dizer que é uma EDIÇÃO, não criação
        form = ConteudoHomeForm(request.POST, instance=conteudo)
        if form.is_valid():
            # Salva o autor da modificação (se tiver usuário logado)
            if request.user.is_authenticated:
                config = form.save(commit=False)
                config.autor_modificacao = request.user
                config.save()
            else:
                form.save()
                
            sucesso = True
    else:
        # Preenche o formulário com o que já existe no banco
        form = ConteudoHomeForm(instance=conteudo)

    return render(request, 'educamais_app/gerenciar_home.html', {
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