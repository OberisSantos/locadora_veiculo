from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404, redirect
from locadora.models import Proprietario, Veiculo, Endereco, Pessoa, Cliente, Funcionario, Locacao, Reserva
from locadora.forms import (
    EnderecoForm, ProprietarioForm, VeiculoForm,  ClienteForm, ReservaForm,
    UsuarioCreationForm, LocacaoForm, FuncionarioForm, ImagensForm
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from braces.views import GroupRequiredMixin #para usar o grupo
from django.contrib.auth.models import Group #para add os grupos
from datetime import datetime 

# Create your views here.
#função geral
@login_required(login_url='page_login')
def buscar(request):
    return render(request, 'locadora/buscar.html', {})


@login_required(login_url='page_login')
def adicionar_imagens(request, id):
    veiculo = get_object_or_404(Veiculo, pk=id)
    if request.method == 'POST':
        form_imagens = ImagensForm(request.POST, request.FILES)
        if form_imagens.is_valid():
            imagens = form_imagens.save(commit=False)
            imagens.veiculo_id = veiculo.id
            imagens.save()

            return redirect(detalhar_veiculo, id=veiculo.id)
    else:
        form_imagens = ImagensForm()
    return render(request, 'locadora/editar_imagens.html', {'form_imagens':form_imagens, 'veiculo':veiculo})


#page inicial
@login_required(login_url='page_login')
def index(request):
    locacao = Locacao.objects.filter().order_by('-data_devolucao') #traz todas as locações e ordena por data_devolução
    locacao_ativa = {}
   
    locacao_pendente = {}

    for locacao in locacao:
        if locacao.status_id == 1:
            locacao_ativa[locacao] = locacao
        elif locacao.status_id == 3:
            locacao_pendente[locacao] = locacao

    #locacao_pendente = Locacao.objects.filter(status_id=2).order_by('-data_devolucao')

    return render(request, 'locadora/index.html', {'locacao':locacao_ativa, 'locacao_pendente':locacao_pendente})


# ------------ CAMPOS PARA A FUNÇÃO LOCAÇÃO ---------------- #
@login_required(login_url='page_login')
def cadastrar_locacao(request, id): #função para cadastrar as locações
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        veiculo = get_object_or_404(Veiculo, pk=id)

        if request.method == 'POST':
            form_locacao = LocacaoForm(request.POST, request.FILES)

            if form_locacao.is_valid():
                locacao = form_locacao.save(commit=False)
                locacao.veiculo_id = veiculo.id #atribuir o veiculo para a locação 
                locacao.valor_diaria = veiculo.valor_locacao #atribuir o valor da diária para a locação
                locacao.km_saida = veiculo.quilometragem #atribuir o valor da diária para a locação

                locacao.save()
                #aqui vai alterar o status do veículo de acordo o status da locaçao
                if locacao.status_id == 1 or locacao.status_id == 3: #ativa
                    veiculo.status_id = 2 #ocupado
                elif locacao.status_id == 2: #finalizada
                    veiculo.status_id = 1 #disponivel
            
                veiculo.save()

                return redirect(detalhar_locacao, id=locacao.id)
        else:
            form_locacao = LocacaoForm()
        objeto = {
            'titulo': 'Locação de Veículo',
            'form_locacao': form_locacao,
            'botao': 'Locar',
            'veiculo': veiculo,        
        }
        return render(request, 'locadora/cadastrar_locacao.html', objeto)
    return redirect(index)


@login_required(login_url='page_login') # o usuário precisa está logado 
def deletar_locacao(request, id):
    #verificar se o usuário logado tem permissão para essa operação
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        locacao = get_object_or_404(Locacao, pk=id)
        mensagem = 'a locação do veículo: '

        if request.method == 'POST':


            if locacao.status_id != 1:            
                locacao.delete()
            elif locacao.status_id == 1 or  locacao.status_id == 3: #ativa
                veiculo = get_object_or_404(Veiculo, pk=locacao.veiculo_id)
                veiculo = get_object_or_404(Veiculo, pk=locacao.veiculo_id)
                veiculo.status_id = 1 #disponivel
                veiculo.save()


            return redirect(listar_locacao)
        else:
           return render(request, 'locadora/delete_confirm.html', {'objeto': locacao, 'mensagem':mensagem}) 
    return render(request, 'locadora/permissao_invalida.html', {}) 


@login_required(login_url='page_login')
def editar_locacao(request, id): #função para cheque-ou
    locacao = get_object_or_404(Locacao, pk=id) #recebe a locação

    if request.method == 'POST':
        form_locacao = LocacaoForm(request.POST, request.FILES, instance=locacao)

        if form_locacao.is_valid(): 
            locacao = form_locacao.save(commit=False)
            locacao.save() #salva as alterações
            if Veiculo.objects.filter(pk=locacao.veiculo_id).exists():
                veiculo = get_object_or_404(Veiculo, pk=locacao.veiculo_id)

                if locacao.status_id == 1 or locacao.status_id == 3: #ativa
                    veiculo.status_id = 2 #ocupado
                elif locacao.status_id == 2: #finalizada
                    
                    if locacao.km_saida <= locacao.km_chegada:
                        veiculo.status_id = 1 #disponivel
                        veiculo.quilometragem = locacao.km_chegada
                    else:
                        objeto = {
                            'titulo': 'Editar Locação',
                            'form_locacao': form_locacao,
                            'locacao': locacao,
                            'botao': 'Editar',
                            'error': 'A km de chegada deve ser maior ou igual a de saída',
                        }
                        return render(request, 'locadora/editar_locacao.html', objeto)
                    
            
                veiculo.save()

            return redirect(detalhar_locacao, id=locacao.id)

    else:
        form_locacao = LocacaoForm(instance=locacao)
    
    objeto = {
        'titulo': 'Editar Locação',
        'form_locacao': form_locacao,
        'locacao': locacao,
        'botao': 'Editar',
    }

    return render(request, 'locadora/editar_locacao.html', objeto)



@login_required(login_url='page_login')
def detalhar_locacao(request, id):
    locacao = get_object_or_404(Locacao, pk=id) 
    return render(request, 'locadora/detalhar_locacao.html', {'locacao':locacao}) 


@login_required(login_url='page_login')
def listar_locacao(request):
    locacao = Locacao.objects.all().order_by('data_devolucao')

    return render(request, 'locadora/listar_locacao.html', {'locacao':locacao})

# ------------ CAMPOS PARA A FUNÇÃO RESERVA ---------------- #
@login_required(login_url='page_login')
def editar_reserva(request, id):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        reserva = get_object_or_404(Reserva, pk=id)
        
        if request.method == 'POST':
            form_reserva = ReservaForm(request.POST, request.FILES, instance=reserva)
            
            if form_reserva.is_valid():
                reserva = form_reserva.save(commit=False)
                reserva.save()

                return redirect(listar_reservas)
        else:
            form_reserva = ReservaForm(instance= reserva)
            objeto = {
                'titulo': 'Editar Reserva',
                'form_reserva': form_reserva,
                'botao': 'Editar',
            }
        return render(request, 'locadora/editar_reserva.html', objeto)

    return render(request, 'locadora/permissao_invalida.html', {})


@login_required(login_url='page_login') #preciso está logado para acessar
def listar_reservas(request):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        reserva = Reserva.objects.all()

        return render(request, 'locadora/listar_reservas.html', {'reserva':reserva})
    return redirect(index)

@login_required(login_url='page_login') #preciso está logado para acessar
def deletar_reserva(request, id):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        reserva = get_object_or_404(Reserva, pk=id)
        mensagem = 'a reserva: '

        if request.method == 'POST':
            reserva.delete()

            return redirect(listar_reservas)
        else:
           return render(request, 'locadora/delete_confirm.html', {'objeto': reserva, 'mensagem':mensagem}) 
    return redirect(index)

# ------------ CAMPOS PARA A CLASSE VEÍCULO ---------------- #
@login_required(login_url='page_login')
def deletar_veiculo(request, id):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        veiculo = get_object_or_404(Veiculo, pk=id)
        mensagem = 'o veículo de placa: '

        if request.method == 'POST':
            veiculo.delete()

            return redirect(listar_veiculos)
        else:
           return render(request, 'locadora/delete_confirm.html', {'objeto': veiculo, 'mensagem':mensagem}) 
    return redirect(index)


@login_required(login_url='page_login') #preciso está logado para acessar
def detalhar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, pk=id)

    return render(request, 'locadora/detalhar_veiculo.html', {'veiculo':veiculo})



@login_required(login_url='page_login') #preciso está logado para acessar
def cadastrar_veiculo(request, id):
    proprietario = get_object_or_404(Proprietario, pk=id)
    if request.method == 'POST':  
        print('post')  
        form_veiculo = VeiculoForm(request.POST, request.FILES)
        if form_veiculo.is_valid():
            veiculo = form_veiculo.save(commit=False)
            veiculo.proprietario_id = proprietario.id
            veiculo.save()

            return redirect(detalhar_veiculo, id=veiculo.id)#tenho que redirecionar para detalhar_veiculo

    else:
        form_veiculo = VeiculoForm()
    
    objeto = {
        'titulo': 'Cadastrar Veículo',
        'form_veiculo': form_veiculo,
        'proprietario': proprietario,
        'botao': 'Cadastrar',
    }

    return render(request, 'locadora/editar_veiculo.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def editar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, pk=id)

    if request.method == 'POST':
        form_veiculo = VeiculoForm(request.POST, request.FILES, instance=veiculo)

        if form_veiculo.is_valid():
            veiculo = form_veiculo.save(commit=False)
            veiculo.save()

            return redirect(detalhar_veiculo, id=veiculo.id)

    else:
        form_veiculo = VeiculoForm(instance=veiculo)
    
    objeto = {
        'titulo': 'Editar Veículo',
        'form_veiculo': form_veiculo,
        'proprietario': veiculo,
        'botao': 'Editar',
    }

    return render(request, 'locadora/editar_veiculo.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def listar_veiculo_disponivel(request):
    veiculo = Veiculo.objects.filter(status=1)

    if veiculo is not None:        
        return render(request, 'locadora/listar_veiculos.html', {'veiculos':veiculo})

    return render(request, 'locadora/listar_veiculos.html', {'veiculos':veiculo})

def veiculo_filter(request, id):
    objeto = {}
    objeto['titulo'] = 'Listar Veículo'

    if request.user.groups.filter(name='Administrador').exists() or request.user.has_module_perms('Administrador'):
        veiculo = Veiculo.objects.filter(proprietario_id=id)
        objeto['veiculos'] = veiculo
        
        return render(request, 'locadora/listar_veiculos.html', objeto)

        
           # return render(request, 'locadora/listar_veiculos.html', objeto)
    return redirect(page_login)
        
@login_required(login_url='page_login') #preciso está logado para acessar
def listar_veiculos(request):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        veiculos = Veiculo.objects.all()

        if veiculos is not None:
            return render(request, 'locadora/listar_veiculos.html', {'veiculos': veiculos, 'existe':True})
        else:
            return render(request, 'locadora/listar_veiculos.html', {'veiculos': veiculos, 'existe':False})
        
    else:
        return redirect(page_login)#criar uma pagina para mostrar usuario sem permissao


# ------------ CAMPOS PARA A CLASSE PROPRIETARIO  ---------------- #

@login_required(login_url='page_login') #preciso está logado para acessar
def buscar_proprietario(request): #buscar funcionario 
    dicionario = {} #cria um dicionario para usar na função de busca
        
    dicionario['titulo'] = 'Buscar Proprietário' 
    dicionario['buscar_por'] = 'CPF'
    dicionario['mascara']='000.000.000-00'

    if (request.method == 'POST'):
        prop = request.POST['buscar']

        try: #recebe um excep e trata
            #proprietario = get_object_or_404(Proprietario, Q(cpf=prop) | Q (nome__icontains=prop))
            proprietario = Proprietario.objects.filter(cpf_cnpj=prop) #filtra o proprietário pela valor passado
            dicionario['proprietario'] = proprietario
            dicionario['titulo'] = 'Listar Proprietário'

            return render(request, 'locadora/listar_proprietario.html', dicionario)
        except: # se apresentar algum erro ele é tratado 
            dicionario['buscar'] = prop
            dicionario['erro'] = True
            return render(request, 'locadora/buscar.html', dicionario)

    else:
        return render(request, 'locadora/buscar.html', dicionario)



@login_required(login_url='page_login') #preciso está logado para acessar
def deletar_proprietario(request, id): #essa funcionalidade só para administrador
    #request.user.groups.filter(name='Administrador').exists() or request.user.has_module_perms('Administrador')
    if request.user.has_module_perms('Administrador'):
        proprietario = get_object_or_404(Proprietario, pk=id)
        
        veiculo = Veiculo.objects.filter(proprietario_id=proprietario.id).count()
        mensagem = 'o proprietário: '
        if veiculo > 0:
            return redirect(veiculo_filter, id=proprietario.id)

        elif request.method == 'POST':
            '''if proprietario.tipo_pessoa == 'PF':
                proprietario = '''
            proprietario.delete()

            return redirect(listar_proprietario)
        else:
            return render(request, 'locadora/delete_confirm.html', {'objeto':proprietario, 'mensagem':mensagem})#redirecionar par uma tela com informação
    mensagem = {
        'mensagem':'Você não tem permissão para efetuar essa operação!'
    }

    return render(request, 'locadora/permissao_invalida.html', mensagem)


@login_required(login_url='page_login') #preciso está logado para acessar
def editar_proprietario(request, id):    
    proprietario = get_object_or_404(Proprietario,pk=id)

    if request.method == 'POST':

        form_prop = ProprietarioForm(request.POST,  request.FILES, instance=proprietario)

        if form_prop.is_valid():
            proprietario = form_prop.save(commit=False)
            proprietario.save()

            return redirect(detalhar_proprietario, id=proprietario.id)
    else:
        form_prop = ProprietarioForm(instance=proprietario)
    
    objeto = {
        'titulo': 'Editar Proprietario',
        'form_prop': form_prop,
        'botao': 'Editar',
    }

    return render(request, 'locadora/editar_pessoa_fisica.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def cadastrar_proprietario_fisico(request):

    if request.method == 'POST':
        #form_ende = EnderecoForm(request.POST, request.FILES)
        form_prop = ProprietarioForm(request.POST, request.FILES)
        if form_prop.is_valid():
            proprietario = form_prop.save(commit=False)
            proprietario.save()

            return redirect(cadastar_endereco, id=proprietario.id)
    else:
        #form_ende = EnderecoForm()
        form_prop = ProprietarioForm()
         
    objeto = {
        'titulo': 'Cadastrar Proprietário',
        'form_prop': form_prop,
        'botao': 'Cadastrar',
    }
    return render(request, 'locadora/editar_pessoa_fisica.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def detalhar_proprietario(request, id):
    #try:
    proprietario = get_object_or_404(Proprietario, pk=id)
    endereco = Endereco.objects.filter(pessoa=proprietario.id)
    veiculo = Veiculo.objects.filter(proprietario=proprietario.id)
    #except:
        #return redirect(index)#se apresentar algum erro
   
    prop = {
        'proprietario': proprietario,
        'endereco': endereco,
        'veiculo': veiculo,
    }

    return render(request, 'locadora/detalhar_proprietario.html', prop)


@login_required(login_url='page_login') #preciso está logado para acessar
def listar_proprietario(request): 

    #if django_user.groups.filter(name = groupname).exists():
    #permissao = request.user.groups.all () #pegar as permissões para o usuário
    objeto = {}
    objeto['titulo'] = 'Proprietário'

    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'): #valida a permissao do usuario em grupo     
        proprietario = Proprietario.objects.all()
        
        objeto['proprietario'] = proprietario
        

        return render(request, 'locadora/listar_proprietario.html', objeto)

    return redirect(autenticar_user)

# ------------ CAMPOS PARA A CLASSE ENDEREÇO ---------------- #

@login_required(login_url='page_login') #preciso está logado para acessar
def cadastar_endereco(request, id):
    pessoa = get_object_or_404(Pessoa, pk=id)

    if request.method == 'POST':
        form_endereco = EnderecoForm(request.POST, request.FILES)
        
        if form_endereco.is_valid():
            endereco = form_endereco.save(commit=False)
            endereco.pessoa_id= pessoa.id
            endereco.save()

            return redirect(index)

    else:
        form_endereco = EnderecoForm()

    objeto = {
        'titulo': 'Cadastrar Endereço',
        'form': form_endereco,
        'botao': 'Cadastrar',   
    }
    return render(request, 'locadora/cadastrar_endereco.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def editar_endereco(request, id):    
    endereco = get_object_or_404(Endereco,pk=id)

    if request.method == 'POST':
        form = EnderecoForm(request.POST, request.FILES, instance=endereco)

        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.save()

            objeto ={
                'titulo':'Alteração de Endereço',
                 
            }

            return render(request, locadora/tela_ok.html, {})
    else:
        form = EnderecoForm(instance=endereco)
    
    objeto = {
        'titulo': 'Editar Endereço',
        'form': form,
        'botao': 'Editar',
    }
    return render(request, 'locadora/cadastrar_endereco.html', objeto)


#-------------CAMPOS PARA A CLASSE DE CLIENTE ------------------#
@login_required(login_url='page_login') #preciso está logado para acessar
def cadastrar_cliente(request):
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST)

        if form_cliente.is_valid():
            cliente = form_cliente.save(commit=False)
            cliente.save()

            return redirect(cadastar_endereco, id=cliente.id)

    form_cliente = ClienteForm()
    objeto = {
        'titulo':'Cadastro de Cliente',
        'form_cliente': form_cliente,
        'botao': 'Cadastrar'
    }
    return render(request, 'locadora/editar_cliente.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST,  request.FILES, instance=cliente)

        if form_cliente.is_valid():
            cliente = form_cliente.save(commit=False)            
            cliente.save()
            return redirect(detalhar_cliente, id=cliente.id)
    else:
        form_cliente = ClienteForm(instance=cliente)
        objeto = {
            'titulo':'Editar Cliente',
            'form_cliente': form_cliente,
            'botao': 'Editar'
        }
    return render(request, 'locadora/editar_cliente.html', objeto)


@login_required(login_url='page_login') #preciso está logado para acessar
def deletar_cliente(request, id):
    if request.user.groups.filter(name='Funcionario').exists() or request.user.has_module_perms('Administrador'):
        cliente = get_object_or_404(Cliente, pk=id)

        locacao = Locacao.objects.filter(cliente_id=cliente.id)

        if request.method ==  'POST':
            cliente.delete()
            return redirect(listar_cliente)
        else:
            conteudos ={
                'mensagem':'o cliente: ',
                'objeto': cliente,
                'restricao': locacao,
                'aviso': 'O cliente possui locação, tem certeza que dejesa excluir?'
            }
            
            return render(request, 'locadora/delete_confirm.html', conteudos)
    return redirect(index)

@login_required(login_url='page_login') #preciso está logado para acessar
def detalhar_cliente(request, id):
    cliente = get_object_or_404(Cliente, pk=id)
    endereco = Endereco.objects.filter(pessoa_id = cliente.id)
    
    return render(request, 'locadora/detalhar_cliente.html', {'cliente':cliente, 'endereco':endereco})
    
@login_required(login_url='page_login') #preciso está logado para acessar
def listar_cliente(request):
    cliente = Cliente.objects.all()    

    return render(request, 'locadora/listar_cliente.html', {'cliente':cliente})


#------------CAMPOS PARA FUNÇÃO DE FUNCIONÁRIO ----------------#
@login_required(login_url='page_login') #preciso está logado para acessar
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form_funcionario = FuncionarioForm(request.POST)

        if form_funcionario.is_valid():
            funcionario = form_funcionario.save(commit=False)
            funcionario.save()

            return redirect(cadastar_endereco, id=funcionario.id)
    form_funcionario = FuncionarioForm()
    objeto = {
        'titulo': 'Cadastro de Funcionário',
        'form_funcionario': form_funcionario,
        'botao': 'Cadastrar'
    }

    return render(request, 'locadora/editar_funcionario.html', objeto)


@login_required(login_url='page_login') #preciso está logado para acessar
def listar_funcionario(request): 
    objeto = {}
    objeto['titulo'] = 'Funcionário'

    if request.user.has_module_perms('Administrador'): #valida a permissao do usuario em grupo     
        funcionario = Funcionario.objects.all()
        
        objeto['funcionario'] = funcionario

        return render(request, 'locadora/listar_funcionario.html', objeto)
        
    elif request.user.groups.filter(name='Funcionario').exists():
        objeto['mensagem']='Você não tem permissão para efeturar essa operação!'
        
        return render(request, 'locadora/permissao_invalida.html', objeto)
    return redirect(page_logout)


@login_required(login_url='page_login') #preciso está logado para acessar
def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, pk=id)

    if request.method == 'POST':
        form_funcionario = FuncionarioForm(request.POST, request.FILES, instance=funcionario)

        if form_funcionario.is_valid():
            funcionario = form_funcionario.save(commit=False)
            funcionario.save()

            objeto ={
                'titulo':'Editar dados do Funcionário',
            }
            return redirect(listar_funcionario)
    else:
        form_funcionario = FuncionarioForm(instance=funcionario)
    objeto = {
        'titulo': 'Editar dados do Funcionário',
        'form_funcionario': form_funcionario,
        'botao': 'Editar',
    }
    return render(request, 'locadora/editar_funcionario.html', objeto)

@login_required(login_url='page_login') #preciso está logado para acessar
def deletar_funcionario(request, id):
        if request.user.has_module_perms('Administrador'):
            funcionario = get_object_or_404(Funcionario, pk=id)
            
            mensagem = 'o funcionário: '

            if request.method == 'POST':
                funcionario.delete()

                return redirect(listar_funcionario)
            else:
                return render(request, 'locadora/delete_confirm.html', {'objeto':funcionario, 'mensagem':mensagem})#redirecionar par uma tela com informação
        
        mensagem = {
            'mensagem':'Você não tem permissão para efetuar essa operação!'
        }
        return render(request, 'locadora/permissao_invalida.html', mensagem)



# ------------ CAMPOS PARA A CLASSE USER E LOGIN ---------------- #
#UsuarioCreationForm
def cadastrar_usuario(request): #todas as vezes que cadastra um novo usuario ele vai para um grupo
    if request.method == 'POST':
        form_usuario = UsuarioCreationForm(request.POST)
        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
            grupo = get_object_or_404(Group, name='Usuario') #verificar o grupo
           
            form_usuario.save() #salvar o usuario

            user.groups.add(grupo) #salvar o grupo para o usuario
           

            return redirect(page_login)
    else:
        form_usuario = UsuarioCreationForm()
    return render(request, 'locadora/cadastrar_usuario.html', {'form_usuario':form_usuario})


def autenticar_user(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        senha = request.POST['password']

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)

            if request.user.groups.filter(name='Funcionario').exists():
                return redirect(index)

            elif request.user.groups.filter(name='Administrador').exists():
                return redirect(index)
            
            else:
                mensagem = {
                    'mensagem':'Você não tem permissão para acessar esse sistema!'
                }
                logout(request)
                return render(request, 'locadora/permissao_invalida.html', mensagem)
        else:
            form_login = AuthenticationForm(request)
    else:
        form_login = AuthenticationForm(request)
    
    return render(request, 'locadora/login.html', {'form_login': form_login})


@login_required(login_url='page_login')
def senha_alterar(request): #função que serve para o usuário logado alter a senha de acesso
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect(logout_usuario)
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'locadora/alterar_senha.html', {'form_senha': form_senha})



def page_login(request):
    if request.user:
        return redirect(page_logout)
    return render(request, 'locadora/login.html', {})

def page_logout(request):
    logout(request)
    return render(request, 'locadora/login.html', {})
