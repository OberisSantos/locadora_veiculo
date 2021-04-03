from django.contrib import admin
from .models import (
    Endereco, Proprietario, Veiculo, 
    ArquivosDados, ImagensVeiculo, Cliente, 
    StatusVeiculo, StatusLocacao, StatusReserva, Locacao, Reserva, Funcionario

)


# Register your models here.

admin.site.register(Veiculo)
admin.site.register(Proprietario)

admin.site.register(Endereco)
admin.site.register(ArquivosDados)
admin.site.register(ImagensVeiculo)
#admin.site.register(Permissao)
#admin.site.register(Perfil)
admin.site.register(Cliente)
admin.site.register(Funcionario)
admin.site.register(Locacao)
admin.site.register(Reserva)
#dados de status
admin.site.register(StatusVeiculo)
admin.site.register(StatusReserva)
admin.site.register(StatusLocacao)
