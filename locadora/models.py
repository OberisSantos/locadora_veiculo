from django.contrib.auth.models import User #user padrao do django
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Create your models here.
#criar uma funcão para cadastro de usuario e senha

#Classes para arquivos

class Pessoa(models.Model):
    TIPO_PESSOA_CHOICES = (
        ('PF', u'Pessoa Fisica'),
        ('PJ', u'Pessoa Jurídica'),
    )

    nome = models.CharField(max_length=255, blank=False, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True, help_text='Celular para contato')
    email = models.EmailField(max_length=100, blank=False, unique=True)
    tipo_pessoa = models.CharField(max_length=100, choices=TIPO_PESSOA_CHOICES, default='PF')
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    UF_CHOICES = (
            ('AC', 'Acre'), 
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MG', 'Minas Gerais'),
            ('MS', 'Mato Grosso do Sul'),
            ('MT', 'Mato Grosso'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PE', 'Pernanbuco'),
            ('PI', 'Piauí'),
            ('PR', 'Paraná'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('RS', 'Rio Grande do Sul'),
            ('SC', 'Santa Catarina'),
            ('SE', 'Sergipe'),
            ('SP', 'São Paulo'),
            ('TO', 'Tocantins')
        )
    rua = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100, blank=False)
    numero = models.CharField(max_length=15)
    cidade = models.CharField(max_length=50, blank=False)
    uf = models.CharField(max_length=2, verbose_name='UF', choices=UF_CHOICES)
    cep = models.CharField(max_length=12, verbose_name='CEP')

    pessoa = models.OneToOneField(Pessoa, blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rua


class ArquivosDados(models.Model): #arquivos de dados
    arquivo = models.FileField(upload_to='locadora/media', blank=True, null=True)    
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_update = models.DateTimeField(auto_now=True)

    def chage_view(self):
        return self.arquivo
 

class Proprietario(Pessoa):
    SEXO_CHOICES = (
            ('M', u'Masculino'),
            ('F', u'Feminino'),
            ('O', u'Outro'),
        )

    ESTADO_CIVIL_CHOICES = (
            ('S', u'Solteiro'),
            ('C', u'Casado'),
            ('D', u'Divorciado'),
            ('V', u'Viúvo'),
        )
    cpf_cnpj = models.CharField(max_length=30, blank=True, null=True, unique=True, verbose_name='CPF/CNPJ')
    data_nascimento_abertura = models.DateField(blank=True, null=True, verbose_name='Data Nascimento / Abertura')
    sexo = models.CharField(max_length=1, blank=True, null=True, choices=SEXO_CHOICES)
    estado_civil = models.CharField(max_length=1, blank=True, null=True, verbose_name='Estado civil', choices=ESTADO_CIVIL_CHOICES)
    observacao = models.TextField(max_length=150, blank=True, null=True)
    #o proprietario não vai ter senha

    def __str__(self):
        return self.nome


class Cliente(Pessoa):
    cpf_cnpj = models.CharField(max_length=30, blank=True, null=True, unique=True, verbose_name='CPF/CNPJ')
    data_nascimento_abertura = models.DateField(blank=True, null=True, verbose_name='Data Nascimento / Abertura')
    sexo = models.CharField(max_length=1, blank=True, null=True)
    estado_civil = models.CharField(max_length=1, blank=True, null=True, verbose_name='Estado civil')
    
    observacao = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome

class StatusVeiculo(models.Model):
    status = models.CharField(max_length=50, blank=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.status

#classe para o veículo
class Veiculo(models.Model):
    placa = models.CharField(max_length=20, blank=False, unique=True)
    renavam = models.CharField(max_length=15, blank=False, unique=True)
    chassi = models.CharField(max_length=30, blank=False, unique=True)
    cor = models.CharField(max_length=100, blank=False)
    ano = models.IntegerField(blank=False)
    n_portas = models.IntegerField(blank=False)
    tipo_combustivel = models.CharField(max_length=100, blank=False)
    cambio = models.CharField(max_length=50, blank=True, null=True)
    quilometragem= models.IntegerField(blank=False)
    nivel_tanque = models.FloatField(blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    valor_locacao = models.FloatField(blank=True)
    imagem_perfil = models.ImageField(upload_to='locadora/media', blank=True, null=True)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.PROTECT, null=True, blank=True)
    #dono_juridico = models.ForeignKey(DonoJuridico, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(StatusVeiculo, on_delete=models.PROTECT)
    observacao = models.TextField(max_length=150, blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.placa

class ImagensVeiculo(models.Model):
    imagem = models.ImageField(upload_to='locadora/media', blank=True, null=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    def chage_view(self):
        return self.imagem



class Funcionario(Pessoa):
    SEXO_CHOICES = (
            ('M', u'Masculino'),
            ('F', u'Feminino'),
            ('O', u'Outro'),
        )

    cpf = models.CharField(max_length=30, blank=True, null=True, unique=True, verbose_name='CPF')
    data_nascimento = models.DateField(blank=True, null=True, verbose_name='Data Nascimento')
    sexo = models.CharField(max_length=1, blank=True, null=True, choices=SEXO_CHOICES)
    estado_civil = models.CharField(max_length=1, blank=True, null=True, verbose_name='Estado civil')
    salario = models.FloatField(blank=True, null=True)
    data_contratacao = models.DateField(blank=True, null=True)
    observacao = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.nome

class StatusLocacao(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True, max_length=150)

    def __str__(self):
        return self.status

#classe para armazenar dados da locação
class Locacao(models.Model):
    veiculo = models.ForeignKey(Veiculo, null=True, on_delete=models.SET_NULL) #recebe o id do veiculo
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)  #recebe o id do cliente
    #funcionario = models.ForeignKey(Funcionario, null=True, on_delete=models.SET_NULL)

    data_locacao = models.DateTimeField(blank=True, null=True)
    hora_locacao = models.TimeField(blank=True, null=True)
    data_devolucao = models.DateTimeField(blank=True, null=True) 
    hora_devolucao = models.TimeField(blank=True, null=True)
    km_saida = models.FloatField(blank=True, null=True)
    km_chegada = models.FloatField(blank=True, null=True)
    valor_diaria = models.FloatField(blank=True, null=True)
    valor_desconto = models.FloatField(blank=True, null=True)
    valor_total = models.FloatField(blank=True, null=True)   #aqui é calculado com base na data de locação
    forma_pagamento = models.CharField(max_length=50 ,blank=True, null=True)  
    arquivo = models.FileField(upload_to='locadora/uploads', blank=True, null=True)
    status = models.ForeignKey(StatusLocacao, blank=True, null=True, on_delete=models.SET_NULL, default=1)
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        
        return self.veiculo.placa
    
    #função para calcular o valor total
    def save(self, *args, **kwargs):        
        self.valor_total = (int((self.data_devolucao - self.data_locacao).days) * self.valor_diaria) - self.valor_desconto
        return super(Locacao, self).save(*args, **kwargs)
    
#colocar os status da locação
class StatusReserva(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True, max_length=150)

    def __str__(self):
        return self.status

class Reserva(models.Model):
    veiculo = models.ForeignKey(Veiculo, null=True, on_delete=models.SET_NULL)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    #funcionario = models.ForeignKey(Funcionario, null=True, on_delete=models.SET_NULL)

    data_inicio = models.DateTimeField(blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    hora_devolucao = models.TimeField(blank=True, null=True)
    valor_diaria = models.FloatField(blank=True, null=True)
    valor_total = models.FloatField(blank=True, null=True) #aqui é calculado com base na data de locação
    status = status = models.ForeignKey(StatusReserva, blank=True, null=True, on_delete=models.SET_NULL, default=1)
    
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.veiculo.placa

        #calculo
    def save(self, *args, **kwargs):
    	self.valor_total = (((self.data_devolucao - self.data_inicio).days) * self.valor_diaria)
    	return super(Reserva, self).save(*args, **kwargs)
