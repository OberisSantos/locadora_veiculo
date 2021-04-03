from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.edit import CreateView
from locadora.models import (
    Proprietario, Veiculo, Endereco, Perfil, 
    Permissao, Pessoa, Reserva, Locacao, Cliente, StatusReserva
    )
from locadora.forms import (EnderecoForm, ProprietarioForm, VeiculoForm, PerfilForm,
 ClienteForm, UsuarioCreationForm, ReservaForm
 )
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import login, logout, authenticate
from braces.views import GroupRequiredMixin #para usar o grupo
from django.contrib.auth.models import Group #para add os grupos

# Create your views here.


def home(request):
    veiculo = Veiculo.objects.filter(status=1)

    
    if Pessoa.objects.filter(usuario_id=request.user.id).exists():
        cliente = Cliente.objects.filter(usuario_id=request.user.id)
    
        if cliente is not None:
            if request.user.groups.filter(name='Usuario').exists():


                #endereco = Endereco.objects.filter(pessoa=cliente)
                #reserva = Reserva.objects.filter(cliente=cliente)
                #locacao = Locacao.objects.filter(cliente=cliente)
               
                return render(request, 'usuario/home.html', {'cliente':cliente, 'veiculo':veiculo})
    
    return render(request, 'usuario/home.html', {'veiculo':veiculo})


def pesquisar_veiculo(request):
    buscar = request.POST['pesquisar']

    print('buscar ', buscar)

    veiculo = Veiculo.objects.filter(
        (Q(marca__contains=buscar)) | 
        (Q(modelo__contains=buscar))| 
        (Q(cor__contains=buscar))| 
        (Q(n_portas__startswith=buscar))| 
        (Q(tipo_combustivel__contains=buscar)), 
        (Q(status=1))
        )
  
    print('novo ', veiculo)
    return render(request, 'usuario/home.html', {'veiculo':veiculo})


@login_required(login_url='login_usuario')
def reservar_veiculo(request, id):

    if Cliente.objects.filter(usuario_id = request.user.id).exists():
        veiculo = get_object_or_404(Veiculo, pk=id)
        cliente = get_object_or_404(Cliente, usuario_id = request.user.id)

        if veiculo is not None and cliente is not None:
            if request.method == 'POST':
                form_reserva = ReservaForm(request.POST, request.FILES)
                
                if form_reserva.is_valid():
                    reserva = form_reserva.save(commit=False)
                    reserva.veiculo_id = veiculo.id 
                    reserva.cliente_id = cliente.id
                    reserva.valor_diaria = veiculo.valor_locacao
                    reserva.status_id = 1
                    
                    reserva.save()

                    return redirect(detalhar_reserva, id=reserva.id)

            else:          
                form_reserva = ReservaForm()
            return render(request, 'usuario/reserva_veiculo.html', {'form_reserva':form_reserva, 'veiculo': veiculo, 'cliente': cliente})
    else:
        return redirect(usuario_cadastro, id=request.user.id)

    return redirect(home)

@login_required(login_url='login_usuario')
def detalhar_reserva(request, id):
    reserva = get_object_or_404(Reserva, pk=id)
    cliente = get_object_or_404(Cliente, usuario_id=request.user.id)
   

    if reserva.cliente_id == cliente.id:
        return render(request, 'usuario/detalhar_reserva.html', {'reserva':reserva})

    return redirect(home)


@login_required(login_url='login_usuario')
def listar_reserva(request):
    try:
        cliente = get_object_or_404(Cliente, usuario_id=request.user.id)
    
        reserva = Reserva.objects.filter(cliente_id=cliente.id)

        return render(request, 'usuario/listar_reseva.html', {'reserva':reserva, 'esiste':True})
    except:
        return render(request, 'usuario/listar_reseva.html', {'esiste':False})

    return redirect(home)

#função para cadastrar dados pessoais do usuário
@login_required(login_url='login_usuario')
def usuario_cadastro(request, id):
    
    if request.method == 'POST':
        form_cliente = ClienteForm(request.POST, request.FILES)
       
        if form_cliente.is_valid():
            cliente = form_cliente.save(commit=False)
            cliente.usuario_id = request.user.id
            cliente.tipo_pessoa = u'PF'
            cliente.save()

            return redirect (home)
        
    else:
        form_cliente= ClienteForm()

    return render(request, 'usuario/asuario_atualizar.html', {'form_cliente':form_cliente})




#função para criar usuario e senha
def criar_usuario(request):
    if request.method == 'POST':
        #form_usuario = UsuarioCreationForm(request.POST)
        form_usuario = UsuarioCreationForm(request.POST)

        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
           
            grupo = get_object_or_404(Group, name='Usuario') #verificar o grupo
            #perfil = Perfil()
            form_usuario.save() #salvar o usuario

            user.groups.add(grupo) #salvar o grupo para o usuario
         
            return redirect(login_usuario)
    else:
        form_usuario = UsuarioCreationForm()
    return render(request, 'usuario/criar_usuario.html', {'form_usuario':form_usuario})

#pagina de autenticação
def autenticar_usuario(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        senha = request.POST['password']

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            form_login = AuthenticationForm(request)
    else:
        form_login = AuthenticationForm(request)
    
    return render(request, 'usuario/login.html', {'form_login': form_login})
      

def login_usuario(request):
    return render(request, 'usuario/login.html', {})

def logout_usuario(request):
    logout(request)
    return render(request, 'usuario/login.html', {})

