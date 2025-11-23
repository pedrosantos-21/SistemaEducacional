from .models import Reeducando, Professor, Curso, Matricula, Progresso
from django.contrib.auth.models import User
from django import forms

class ReeducandoForm(forms.ModelForm):
   class Meta:
        model = Reeducando
        fields = [
            'nome_completo', 'alcunha', 'cpf', 'rg', 'nome_pai', 'nome_mae',
            'data_nascimento', 'nacionalidade', 'estado_civil', 'pena_aplicada',
            'regime_inicial', 'data_prisao', 'data_prevista_termino', 
            'status', 'observacoes'
        ]
        
        # AQUI ESTÁ O SEGREDO DO PLACEHOLDER
        widgets = {
            'nome_completo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome Completo do Reeducando'
            }),
            
            'cpf': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '000.000.000-00' # Máscara visual
            }),
            
            'rg': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Digite o RG'
            }),

            # Para datas, o type='date' já cria o calendário do navegador
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date' 
            }),
            
            'data_prisao': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            
            'data_prevista_termino': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),

            'pena_aplicada': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: 5 anos, 3 meses'
            }),
            
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Insira observações adicionais aqui...',
                'rows': 3  # Altura da caixa de texto
            }),

            # Para Selects (Dropdowns), usamos apenas a classe, pois não tem placeholder padrão
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'regime_inicial': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class ProfessorForm(forms.ModelForm):
    senha_login = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        label='Senha de Acesso'
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita a senha'}),
        label='Confirmar Senha'
    )

    class Meta:
        model = Professor
        fields = ['nome_completo', 'cpf', 'rg', 'data_nascimento', 'email', 'telefone',
            'area_atuacao', 'formacao_academica', 'disciplinas_ministradas', 'status', 'observacoes']
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Professor'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'professor@educamais.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) 9XXXX-XXXX'}),
            'area_atuacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Exatas, Humanas'}),
            'formacao_academica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Licenciatura em Matemática'}),
            'disciplinas_ministradas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Matemática I, Lógica...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # ATENÇÃO AQUI: O 'def' tem que estar alinhado com o 'class Meta' acima
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha_login")
        confirmar = cleaned_data.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            # Isso joga o erro lá para o campo "Confirmar Senha" em vez do topo
            self.add_error('confirmar_senha', "As senhas não conferem.")

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = [
            'nome_curso', 'descricao_ementa', 'professor_responsavel',
            'carga_horaria', 'modalidade', 'modulos_aulas', 'status'
        ]

        widgets = {
            'nome_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Introdução à Informática'}),
            'descricao_ementa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'carga_horaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 40h'}),
            'modalidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Presencial / EAD'}),
            'modulos_aulas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Módulo 1: ...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            # O professor_responsavel é um Select, o Django popula ele automaticamente
            'professor_responsavel': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Regra de négocio do RF005: Mostra apenas professores ativos (Status='1')
        self.fields['professor_responsavel'].queryset = Professor.objects.filter(status='1')


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'curso', 'status'] # Data de início é automática
        
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # REGRA DE NEGÓCIO: Só permitir matricular alunos ATIVOS e cursos ATIVOS
        self.fields['aluno'].queryset = Reeducando.objects.filter(status=1) 
        self.fields['curso'].queryset = Curso.objects.filter(status='1')


class ProgressoForm(forms.ModelForm):
    class Meta:
        model = Progresso
        fields = ['matricula', 'modulo_aula', 'nota_avaliacao', 'tempo_gasto']
        
        widgets = {
            'matricula': forms.Select(attrs={'class': 'form-select'}),
            'modulo_aula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Módulo 1 - Introdução'}),
            'nota_avaliacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.0 a 10.0', 'step': '0.1', 'min': '0', 'max': '10'}),
            'tempo_gasto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # REGRA DE NEGÓCIO: Só mostra matrículas "Em Andamento" (Status=1)
        self.fields['matricula'].queryset = Matricula.objects.filter(status='1')