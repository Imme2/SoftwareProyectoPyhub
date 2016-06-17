# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 06:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='billetera',
            fields=[
                ('idBilletera', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(default=None, max_length=50)),
                ('balance', models.DecimalField(decimal_places=3, default=0, max_digits=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='billetera', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='contiene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ingrediente',
            fields=[
                ('idIngr', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('cantidad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('idItem', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=1)),
                ('precio', models.DecimalField(decimal_places=3, max_digits=30)),
                ('foto', models.CharField(max_length=300)),
                ('descripcion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='menu',
            fields=[
                ('idMenu', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('contieneRel', models.ManyToManyField(through='Registro.contiene', to='Registro.item')),
            ],
        ),
        migrations.CreateModel(
            name='ofrece',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.PositiveIntegerField()),
                ('idRest', models.PositiveIntegerField()),
                ('idIngr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='orden',
            fields=[
                ('nroOrden', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('totalPagado', models.DecimalField(decimal_places=3, default=0, max_digits=30)),
            ],
        ),
        migrations.CreateModel(
            name='ordenActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='parametro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idParam', models.PositiveIntegerField()),
                ('horarioCierre', models.TimeField()),
                ('horarioEntrada', models.TimeField()),
                ('cantPuestos', models.PositiveIntegerField()),
                ('menuActual', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu', to='Registro.menu')),
            ],
        ),
        migrations.CreateModel(
            name='pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idRest', models.PositiveIntegerField()),
                ('idIngr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.ingrediente')),
                ('usernameA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.administrador')),
            ],
        ),
        migrations.CreateModel(
            name='perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.CharField(blank=True, max_length=10, null=True)),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, null=True)),
                ('fechaNac', models.DateField(blank=True, null=True)),
                ('foto', models.CharField(blank=True, max_length=300, null=True)),
                ('tlf', models.CharField(blank=True, max_length=17, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='posee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('idIngr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.ingrediente')),
                ('idItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.item')),
            ],
        ),
        migrations.CreateModel(
            name='proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreEmpr', models.CharField(max_length=40)),
                ('rif', models.CharField(max_length=10)),
                ('ofreceRel', models.ManyToManyField(through='Registro.ofrece', to='Registro.ingrediente')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='proveedor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='realiza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroOrden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.orden')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='tiene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.item')),
                ('nroOrden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.orden')),
            ],
        ),
        migrations.CreateModel(
            name='tieneActual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.item')),
                ('nroOrden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.ordenActual')),
            ],
        ),
        migrations.CreateModel(
            name='transaccion',
            fields=[
                ('idTrans', models.AutoField(primary_key=True, serialize=False)),
                ('monto', models.DecimalField(decimal_places=3, max_digits=30)),
                ('fecha', models.DateField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='usernameP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.proveedor'),
        ),
        migrations.AddField(
            model_name='ordenactual',
            name='tieneRel',
            field=models.ManyToManyField(through='Registro.tieneActual', to='Registro.item'),
        ),
        migrations.AddField(
            model_name='ordenactual',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ordenActual', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orden',
            name='tieneRel',
            field=models.ManyToManyField(through='Registro.tiene', to='Registro.item'),
        ),
        migrations.AddField(
            model_name='orden',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ofrece',
            name='usernameP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.proveedor'),
        ),
        migrations.AddField(
            model_name='item',
            name='poseeRel',
            field=models.ManyToManyField(through='Registro.posee', to='Registro.ingrediente'),
        ),
        migrations.AddField(
            model_name='contiene',
            name='idItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.item'),
        ),
        migrations.AddField(
            model_name='contiene',
            name='idMenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.menu'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='idIngr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.ingrediente'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.proveedor'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='idMenu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.menu'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrador',
            name='idParam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.parametro'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='administrador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administrador',
            name='usernameP',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registro.proveedor'),
        ),
        migrations.AlterUniqueTogether(
            name='realiza',
            unique_together=set([('username', 'nroOrden')]),
        ),
        migrations.AlterUniqueTogether(
            name='posee',
            unique_together=set([('idItem', 'idIngr')]),
        ),
        migrations.AlterUniqueTogether(
            name='pedido',
            unique_together=set([('usernameP', 'usernameA', 'idIngr')]),
        ),
        migrations.AlterUniqueTogether(
            name='ofrece',
            unique_together=set([('usernameP', 'idIngr')]),
        ),
        migrations.AlterUniqueTogether(
            name='contiene',
            unique_together=set([('idMenu', 'idItem')]),
        ),
        migrations.AlterUniqueTogether(
            name='consulta',
            unique_together=set([('username', 'idIngr')]),
        ),
    ]
