from django.db import models
from django.contrib.auth.models import User  # <--- IMPORTANTE: Importamos o usuário padrão do Django
import uuid  # Importe isso lá no topo do arquivo para gerar códigos únicos

class Reeducando(models.Model):
    
    # ... (Mantenha o código do Reeducando EXATAMENTE como estava no seu, não mudou nada) ...
    # Vou resumir aqui para não ficar gigante, mas pode manter o seu bloco Reeducando inteiro.
    ESTADO_CIVIL_CHOICES = [
        ('SOLTEIRO', 'Solteiro(a)'),
        ('CASADO', 'Casado(a)'),
        ('DIVORCIADO', 'Divorciado(a)'),
        ('VIUVO', 'Viúvo(a)'),
        ('UNIAO_ESTAVEL', 'União Estável'),
    ]
    REGIME_CHOICES = [
        (1, 'Fechado'),
        (2, 'Semi-aberto'),
        (3, 'Aberto'),
        (4, 'Provisório')
    ] # -> Lista de tuplas (valor, rotulo)
    
    STATUS_ALUNO_CHOICES = [
        (1, 'Ativo'),
        (2, 'Inativo'),
        (3, 'Transferido'),
        (4, 'Egresso')
    ]

    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    alcunha = models.CharField(max_length=50, blank=True, null=True, verbose_name="Alcunha/Apelido")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, verbose_name="RG")
    nome_pai = models.CharField(max_length=255, verbose_name="Nome do Pai")
    nome_mae = models.CharField(max_length=255, verbose_name="Nome da Mãe")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    nacionalidade = models.CharField(max_length=100, default='Brasileira')
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    pena_aplicada = models.CharField(max_length=100, blank=True, null=True, verbose_name="Pena Aplicada")
    regime_inicial = models.IntegerField(choices=REGIME_CHOICES, verbose_name="Regime Inicial")
    data_prisao = models.DateField(verbose_name="Data de Prisão")
    data_prevista_termino = models.DateField(verbose_name="Data Prevista de Término")
    status = models.IntegerField(choices=STATUS_ALUNO_CHOICES, default=1)
    data_cadastro = models.DateField(auto_now_add=True, verbose_name="Data de Cadastro")
    observacoes = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Observações")

    def __str__(self):
        return f"{self.nome_completo} - {self.cpf}"


class Professor(models.Model):
    """
    RF002 - Cadastro do Professor.
    AJUSTE INTELIGENTE: Vinculado ao User do Django para login seguro.
    """
    # Vínculo 1-para-1 com o sistema de autenticação do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário do Sistema", null=True, blank=True)
    
    STATUS_PROF_CHOICES = [(1, 'Ativo'), (2, 'Inativo'), (3, 'Afastado')]

    # Dados Pessoais (Removemos login/senha manuais, pois estão no 'usuario' acima)
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    email = models.EmailField(verbose_name="E-mail") # Pode ser usado para recuperar senha
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    # Dados Profissionais
    area_atuacao = models.CharField(max_length=100, verbose_name="Área de Atuação")
    formacao_academica = models.CharField(max_length=100, verbose_name="Formação Acadêmica")
    disciplinas_ministradas = models.TextField(blank=True, null=True, help_text="Listar disciplinas separadas por vírgula")
    
    status = models.IntegerField(choices=STATUS_PROF_CHOICES, default=1)
    data_cadastro = models.DateField(auto_now_add=True)
    observacoes = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"


class Curso(models.Model):
    """
    RF005 - Gestão de Cursos.
    """
    STATUS_CURSO_CHOICES = [('1', 'Ativo'), ('2', 'Em Desenvolvimento'), ('3', 'Inativo')]

    nome_curso = models.CharField(max_length=255, verbose_name="Nome do Curso/Disciplina")
    descricao_ementa = models.TextField(verbose_name="Descrição/Ementa")
    
    professor_responsavel = models.ForeignKey(
        Professor, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Professor Responsável"
    )
    
    carga_horaria = models.CharField(max_length=50, verbose_name="Carga Horária Total")
    modalidade = models.CharField(max_length=50, blank=True, null=True)
    
    # AJUSTE: Mantive textfield, mas no futuro podemos mudar para FileField se quiser upload real
    modulos_aulas = models.TextField(blank=True, null=True, verbose_name="Conteúdo/Módulos")
    
    status = models.CharField(max_length=1, choices=STATUS_CURSO_CHOICES, default='1')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_curso

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class Matricula(models.Model):
    """
    RF008 - Requisito responsável pela Matrícula de Alunos em Cursos.
    """
    # Padrão definido no RF008: 1=Em andamento, 2=Concluído, 3=Trancado, 4=Evadido
    STATUS_MATRICULA_CHOICES = [
        (1, 'Em Andamento'),
        (2, 'Concluído'),
        (3, 'Trancado'),
        (4, 'Evadido'),
    ]

    # --- VÍNCULOS (FOREIGN KEYS) ---
    # O ID da Matrícula é gerado automaticamente pelo Django (Integer) 
    
    # Vínculo com RF001 (Aluno) - Campo Obrigatório 
    aluno = models.ForeignKey(
        Reeducando, 
        on_delete=models.CASCADE, 
        verbose_name="Aluno"
    )
    
    # Vínculo com RF005 (Curso) - Campo Obrigatório 
    curso = models.ForeignKey(
        Curso, 
        on_delete=models.CASCADE, 
        verbose_name="Curso"
    )
    
    # --- DATAS E SITUAÇÃO ---
    # Data de Início gerada automaticamente pelo sistema 
    data_inicio = models.DateField(auto_now_add=True, verbose_name="Data de Início")
    
    # Data de Conclusão deve ser nula até que o status seja "Concluído" 
    data_conclusao = models.DateField(blank=True, null=True, verbose_name="Data de Conclusão")
    
    # Status padrão deve ser "Em andamento" (1) ao criar 
    status = models.IntegerField(
        choices=STATUS_MATRICULA_CHOICES, 
        default=1, 
        verbose_name="Status da Matrícula"
    )

    def __str__(self):
        return f"{self.aluno.nome_completo} - {self.curso.nome_curso}"

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        # Regra de Negócio: Impede duplicidade (O mesmo aluno no mesmo curso)
        unique_together = ('aluno', 'curso')

# ... (Mantenha o código anterior) ...

class Progresso(models.Model):
    """
    RF009 - Registro de Progresso e Avaliações do Aluno.
    Registra cada aula concluída, nota e tempo de estudo.
    """
    # Vínculo com a Matrícula (RF008) - Obrigatório
    matricula = models.ForeignKey(
        Matricula, 
        on_delete=models.CASCADE, 
        verbose_name="Matrícula do Aluno"
    )
    
    # Identificação da Aula/Módulo (Como no curso usamos TextField, aqui usamos String ou Int)
    modulo_aula = models.CharField(max_length=100, verbose_name="Módulo/Aula Concluída")
    
    # Avaliação (Opcional, pois pode ser apenas uma aula assistida sem prova)
    nota_avaliacao = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name="Nota Obtida"
    )
    
    # Controle de Sincronização e Tempo
    data_conclusao = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora Conclusão")
    tempo_gasto = models.DurationField(blank=True, null=True, verbose_name="Tempo de Estudo") # Ex: 01:30:00
    
    # Status de Sincronização (RF009)
    SYNC_CHOICES = [(1, 'Pendente'), (2, 'Sincronizado')]
    status_sincronizacao = models.IntegerField(choices=SYNC_CHOICES, default=2) # Default 2 pois estamos na web

    def __str__(self):
        return f"{self.matricula.aluno.nome_completo} - {self.modulo_aula}"

    class Meta:
        verbose_name = "Progresso / Nota"
        verbose_name_plural = "Progresso Acadêmico"

import uuid # Importe isso lá no topo do arquivo para gerar códigos únicos

# ... (Seus models anteriores) ...

class Certificado(models.Model):
    """
    Parte do RF010 - Registro de Certificados Emitidos.
    Armazena o histórico de conclusões para consulta posterior.
    """
    # Vínculo com a Matrícula (que já tem Aluno e Curso)
    matricula = models.ForeignKey(
        Matricula, 
        on_delete=models.CASCADE, 
        verbose_name="Matrícula"
    )
    
    # Código único para validação (Ex: a0eebc99-9c0b...)
    codigo_validacao = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True, 
        verbose_name="Código de Validação"
    )
    
    data_emissao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Emissão")
    
    # Opcional: Se quiser salvar o caminho do arquivo PDF gerado
    arquivo_pdf = models.CharField(max_length=255, blank=True, null=True, verbose_name="Caminho do Arquivo")

    def __str__(self):
        return f"Certificado {self.codigo_validacao} - {self.matricula.aluno.nome_completo}"

    class Meta:
        verbose_name = "Certificado Emitido"
        verbose_name_plural = "Certificados Emitidos"

'''
1º O que ela faz?

Class Meta: Dentro do models.py serve para definir metadados do modelo, ou seja, "dados sobre os dados".
            Ela  não cria colunas no banco de dados(como nome,cpf,status), mas diz ao Django como esse modelo deve se comportar ou ser exibido 

2º Onde ela está sendo referenciada?

Ela é usada automaticamente pelo própio Django, pricipalmente em dois lugares:

    A) No admin do Django: Para definir como o modelo será exibido na interface administrativa.
        
      - Quando acessamos o admin do Django (/admin), o Django lê essa class Meta para montar o menu lateral.

        a) Sem Class Meta:
            - O menu mostraria EDUCAMAIS_APP > professors
        b) Com Class Meta:
            - O menu mostrará EDUCAMAIS-APP > Professores

    B) Em mensagens de Erro e formulários.

     - Quando o formulário automático for criado, se houver um erro, o Django pode usar esse nome para dizer: 
            "Ocorreu um erro ao salvar o Professor"
     - Em vez de usar o nome técnico da classe.


     

'''