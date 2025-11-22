# Arquivo: educamais_app/urls.py
from django.urls import path
from . import views  # Importa as views que estão na mesma pasta

urlpatterns = [
    # Rota para a página inicial (http://127.0.0.1:8000/)
    path('', views.home, name='home'), 
    
    # Rota para o cadastro (http://127.0.0.1:8000/cadastro/)
    path('cadastro/', views.cadastro_aluno, name='cadastro_aluno'),
]