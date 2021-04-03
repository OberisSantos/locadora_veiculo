# Generated by Django 3.1.7 on 2021-03-24 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locadora', '0008_auto_20210324_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='proprietario',
            name='usuario',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
