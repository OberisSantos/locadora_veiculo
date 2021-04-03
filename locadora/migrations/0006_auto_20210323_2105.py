# Generated by Django 3.1.7 on 2021-03-24 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locadora', '0005_auto_20210323_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusLocacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('observacao', models.TextField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusReserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('observacao', models.TextField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='categoria_cnh',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='numero_cnh',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='validade_cnh',
        ),
        migrations.AddField(
            model_name='cliente',
            name='cnpj',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='data_abertura',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Abertura'),
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('hora_devolucao', models.TimeField(blank=True, null=True)),
                ('valor_diaria', models.FloatField(blank=True, null=True)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.cliente')),
                ('status', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.statusreserva')),
                ('veiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.veiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Locacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_locacao', models.DateField()),
                ('hora_locacao', models.TimeField()),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('hora_devolucao', models.TimeField(blank=True, null=True)),
                ('km_saida', models.FloatField(blank=True, null=True)),
                ('km_chegada', models.FloatField(blank=True, null=True)),
                ('valor_diaria', models.FloatField(blank=True, null=True)),
                ('valor_seguro', models.FloatField(blank=True, null=True)),
                ('valor_desconto', models.FloatField(blank=True, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_cnh', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Nº CNH')),
                ('validade_cnh', models.DateField(blank=True, unique=True, verbose_name='Validade CNH')),
                ('categoria_cnh', models.CharField(blank=True, max_length=5, null=True, verbose_name='Categoria CNH')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='locadora/dados')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('data_update', models.DateTimeField(auto_now=True, null=True)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.cliente')),
                ('status', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.statuslocacao')),
                ('veiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locadora.veiculo')),
            ],
        ),
    ]
