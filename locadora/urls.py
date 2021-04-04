"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views

urlpatterns = [
    path('home', views.index, name='index'),

    #usuario
    path('cadastrar_usuario', views.cadastrar_usuario, name="cadastrar_usuario"),

    #login, logou e atutenticar
    path('', views.page_login, name='page_login'),
    path('logout', views.page_logout, name='page_logout'),
    path('autenticar/usuario', views.autenticar_user, name='autenticar_user'),

    #path table veiculos
    path('veiculo/listar', views.listar_veiculos, name='listar_veiculos'),
    path('veiculo/filter/<int:id>/', views.veiculo_filter, name='filtrar_veiculo'),
    path('veiculo/new/<int:id>/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('veiculo/<int:id>', views.detalhar_veiculo, name='detalhar_veiculo'),
    path('veiculo/disponivel', views.listar_veiculo_disponivel, name='listar_veiculo_disponivel'),
    path('veiculo/deletar/<int:id>', views.deletar_veiculo, name='deletar_veiculo'),
    path('veiculo/editar/<int:id>', views.editar_veiculo, name='editar_veiculo'),

    #path proprietário
    path('proprietario/listar', views.listar_proprietario, name='listar_proprietario'),
    path('proprietario/<int:id>/', views.detalhar_proprietario, name='detalhar_proprietario'),
    path('proprietario/new/', views.cadastrar_proprietario_fisico, name='cadastrar_proprietario_fisico'),
    path('proprietario/editar/<int:id>/', views.editar_proprietario, name='editar_proprietario'),
    path('proprietario/buscar', views.buscar_proprietario, name='buscar_proprietario'),
    path('proprietario/deletar/<int:id>/', views.deletar_proprietario, name='deletar_proprietario'),
    
    #path endereco
    path('endereco/new/<int:id>/', views.cadastar_endereco, name='cadastar_endereco'),
    path('endereco/editar/<int:id>/', views.editar_endereco, name='editar_endereco'),

    #path cliente
    path('cliente/new/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('cliente/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/deletar/<int:id>/', views.deletar_cliente, name='deletar_cliente'),
    path('cliente/listar', views.listar_cliente, name='listar_cliente'),
    path('cliente/<int:id>/', views.detalhar_cliente, name='detalhar_cliente'),

    #path Funcionario
    path('funcionario/new', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('funcionario/listar', views.listar_funcionario, name='listar_funcionario'),
    path('funcionario/editar/<int:id>', views.editar_funcionario, name='editar_funcionario'),
    path('funcionario/deletar/<int:id>/', views.deletar_funcionario, name='deletar_funcionario'),


    #path para locação
    path('locacao/new/<int:id>', views.cadastrar_locacao, name='cadastrar_locacao'),
    path('locacao/listar', views.listar_locacao, name='listar_locacao'),
    path('locacao/<int:id>/', views.detalhar_locacao, name='detalhar_locacao'),
    path('locacao/deletar/<int:id>', views.deletar_locacao, name='deletar_locacao'),
    path('locacao/editar/<int:id>', views.editar_locacao, name='editar_locacao'),

    #path para reserva
    path('listar/reserva', views.listar_reservas, name='listar_reservas'),
    path('reserva/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),

    #path geral
    path('buscar', views.buscar, name='buscar'),
    #path('perfil', views.buscar_perfil, name='buscar_perfil'),
]