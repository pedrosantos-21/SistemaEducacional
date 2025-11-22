# Arquivo: educamais_app/views.py
from django.shortcuts import render

def home(request):
    # Por enquanto vamos renderizar o cadastro na home também, ou uma página temporária
    return render(request, 'educamais_app/cadastro_aluno.html') 

def cadastro_aluno(request):
    return render(request, 'educamais_app/cadastro_aluno.html')