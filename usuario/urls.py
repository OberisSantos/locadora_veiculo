from django.urls import path
from usuario import views

urlpatterns = [
    path('', views.home, name='home'),
    path('veiculo/pesquisar', views.pesquisar_veiculo, name='pesquisar_veiculo'),

    path('login', views.login_usuario, name='login_usuario'),
    path('logout', views.logout_usuario, name='logout_usuario'),
    path('autenticar/usuario', views.autenticar_usuario, name='autenticar_usuario'),
    path('usuario/criar', views.criar_usuario, name='criar_usuario'),

    path('usuario/cadastro/', views.usuario_cadastro,  name='usuario_cadastro'),
    path('usuario/editar/', views.usuario_editar, name='usuario_editar'),

    path('endereco/editar/', views.endereco_editar, name='endereco_editar'),
    path('endereco/cadastro/', views.endereco_cadastro, name='endereco_cadastro'),

    path('veiculo/reservar/<int:id>', views.reservar_veiculo, name='reservar_veiculo'),
    path('reserva/detalhe/<int:id>', views.detalhar_reserva, name='detalhar_reserva'),
    path('reserva/listar', views.listar_reserva, name='listar_reserva'),

]