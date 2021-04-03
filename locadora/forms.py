from django import forms
from datetime import datetime
from django.contrib.auth.models import User #user padrao do django
from locadora.models import Proprietario, Veiculo, StatusVeiculo, Endereco, Perfil, ImagensVeiculo, Pessoa, Cliente, Locacao, Reserva, Funcionario
from django.contrib.auth.forms import UserCreationForm

#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import User

class UsuarioCreationForm(UserCreationForm): #usei apensa para teste
    class Meta:
        model = User

        fields = ('username', 'password1', 'password2')
        widgets = {
            'username':  forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'password1':  forms.PasswordInput(attrs={
                'class': 'form-control'
            }),
            'password2':  forms.PasswordInput(attrs={
                'class': 'form-control'
            }),
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('usuario', 'permissao')
       
        widgets = {
           'usuario':  forms.Select(attrs={
                'class': 'form-control'
            }),
            'permissao':  forms.Select(attrs={
                'class': 'form-control'
            }),
        }




class EnderecoForm(forms.ModelForm):
    class Meta:

        model = Endereco
        fields = ('rua', 'bairro', 'numero', 'cep', 'cidade', 'uf')

        widgets = {
            'rua': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe a rua:"
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe o bairo:"
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe o número:",
                'disabled':False
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'data-mask':'00000-000'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'uf': forms.Select(attrs={
                    'class': 'form-control'
                } 
            )

        }

class ProprietarioForm(forms.ModelForm):
    class Meta:

        model = Proprietario

        fields = ('nome', 'celular', 'email', 'cpf_cnpj', 'data_nascimento_abertura', 'sexo', 'estado_civil', 'observacao')

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Escreva seu nome:"
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe o telefone:",
                'required':'True',
                'data-mask':'(00)00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required':'True'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'required':'True',
                'data-mask':'000.000.000-00'
            }),
            'data_nascimento_abertura': forms.DateInput(attrs={
                'class': 'form-control',
                'type':"date",
                'required':'True'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Observações'
            }),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
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

        model = Cliente

        fields = ('nome', 'celular', 'email', 'cpf_cnpj', 'data_nascimento_abertura', 'sexo', 'estado_civil', 'observacao')

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Escreva seu nome:"
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe o telefone:",
                'required':'True',
                'data-mask':'(00)00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required':'True'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'required':'True',
                'data-mask':'000.000.000-00'
            }),
            'data_nascimento_abertura': forms.DateInput(attrs={
                'class': 'form-control',
                'type':"date",
                'required':'True'
            }),
            'sexo': forms.Select(choices=SEXO_CHOICES, attrs={
                'class': 'form-control'
            }),
            'estado_civil': forms.Select(choices=ESTADO_CIVIL_CHOICES, attrs={
                'class': 'form-control'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Observações'
            }),
        }


class FuncionarioForm(forms.ModelForm):
    class Meta:
        ESTADO_CIVIL_CHOICES = (
            ('S', u'Solteiro'),
            ('C', u'Casado'),
            ('D', u'Divorciado'),
            ('V', u'Viúvo'),
        )

        model = Funcionario

        fields = ('nome', 'celular', 'email', 'usuario','cpf', 'data_nascimento', 'sexo', 'estado_civil', 'salario', 'data_contratacao' ,'observacao')

        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-control',
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Nome completo:"
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':"Informe o telefone:",
                'required':'True', 
                'data-mask':'(00)00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'required':'True'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'required':'True',
                'data-mask':'000.000.000-00'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type':"date"
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estado_civil': forms.Select(choices=ESTADO_CIVIL_CHOICES, attrs={
                'class': 'form-control'
            }),
            'salario': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'data_contratacao': forms.DateInput(attrs={
                'class': 'form-control',
                'type':"date"
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Observações'
            }),
        }



class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        CAMBIO_CHOICES = (
            ('AUTOMÁTICO', 'Câmbio manual ou mecânico'),
            ('MANUAL/MECÂNICO', 'Câmbio automático'), 
            ('CVT ', 'Transmissão Continuamente Variável'),
            ('AUTOMATIZADO DE DUPLA EMBREAGEM', 'Câmbio automatizado com embreagem dupla'),
        )
        fields = ('placa', 'renavam', 'chassi', 'ano', 'cor', 'n_portas', 'tipo_combustivel', 'cambio', 'quilometragem', 'nivel_tanque', 'modelo', 'marca','valor_locacao', 'proprietario', 'imagem_perfil', 'status', 'observacao')

        widgets = {
            'placa': forms.TextInput(attrs={'class':'form-control'}),
            'renavam': forms.TextInput(attrs={'class':'form-control'}),
            'chassi': forms.TextInput(attrs={'class':'form-control'}),
            'cor': forms.TextInput(attrs={'class':'form-control'}),
            'ano': forms.TextInput(attrs={'class':'form-control'}),
            'n_portas': forms.TextInput(attrs={'class':'form-control'}),
            'modelo': forms.TextInput(attrs={'class':'form-control'}),
            'marca': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_combustivel': forms.TextInput(attrs={'class':'form-control'}),
            'cambio': forms.Select(choices=CAMBIO_CHOICES, attrs={'class': 'form-control'}),
            'quilometragem': forms.TextInput(attrs={'class':'form-control'}),
            'nivel_tanque': forms.TextInput(attrs={'class':'form-control'}),
            'valor_locacao': forms.TextInput(attrs={'class':'form-control'}),
            'proprietario': forms.Select(attrs={'class':'form-control'}),
            'imagem_perfil': forms.FileInput(attrs={}),
            'status': forms.Select(attrs={'class':'form-control'}),
            'observacao': forms.Textarea(attrs={'class':'form-control'}),
                        
        }


class LocacaoForm(forms.ModelForm):
    class Meta:
        
        FORMA_PAGAMENTO_CHOICES  = (
            ('DINHERIO', 'DINHERIO'),
            ('CARTAO/CREDITO', 'CARTÃO DE CRÉDITO'), 
            ('CARTAO/DEBIDO ', 'TCARTÃO DE DÉBITO'),
            ('CHEQUE', 'CHEQUE'),
        )
        
        model = Locacao

        fields = ('cliente', 'data_locacao', 'hora_locacao', 'data_devolucao', 'hora_devolucao', 'km_chegada', 'valor_desconto', 'forma_pagamento', 'arquivo', 'status')

        widgets = {
                'cliente': forms.Select(attrs={
                    'class': 'form-control'
                }),
                'data_locacao': forms.DateInput(attrs={
                    'class': 'form-control',
                    'type':'date'
                }),
                'hora_locacao': forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type':'time',
                }),
                'data_devolucao': forms.DateInput(attrs={
                    'class': 'form-control',
                    'type':'date'
                }),
                'hora_devolucao': forms.TimeInput(attrs={
                    'class': 'form-control',
                    'type':'time',
                }),
                'km_chegada': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'number'
                }),
                'valor_desconto': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'number', 
                    'required':'True'
                }),
                'forma_pagamento': forms.Select(choices=FORMA_PAGAMENTO_CHOICES, attrs={
                    'class': 'form-control'
                }),
                'arquivo': forms.FileInput(attrs={
                    'class': 'form-control'
                }),
                'status': forms.Select(attrs={
                    'class': 'form-control'
                }),
        }


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = ('data_inicio', 'data_devolucao', 'status')

        widgets = {
                'data_inicio': forms.DateInput(attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
                
                'data_devolucao': forms.DateInput(attrs={
                    'class': 'form-control',
                    'type': 'date'
                }),
                'status': forms.Select(attrs={
                    'class': 'form-control',
                }),
               
        }

