# Arquivo: educamais_app/urls.py
from django.urls import path
from . import views  # Importa as views que estão na mesma pasta

urlpatterns = [
    # Rota para a página inicial (http://127.0.0.1:8000/)
    path('', views.home, name='home'), 
    
    # Rota para o cadastro (http://127.0.0.1:8000/cadastro/)
    path('cadastro_aluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('cadastro_professor/', views.cadastro_professor, name='cadastro_professor'),
    path('cadastro_curso/', views.cadastro_curso, name='cadastro_curso'),
    path('cadastro_matricula/', views.cadastro_matricula, name='cadastro_matricula'),
    path('lancamento_nota/', views.lancamento_nota, name='lancamento_nota'),
    path('relatorios/', views.painel_relatorios, name='painel_relatorios'),
]