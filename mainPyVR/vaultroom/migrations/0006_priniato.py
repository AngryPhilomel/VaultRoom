# Generated by Django 2.2.4 on 2019-10-23 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaultroom', '0005_move'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priniato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Количество принятого товара')),
                ('time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время приемки')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vaultroom.Products', verbose_name='Принятый товар')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vaultroom.Storages', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Принятый товар',
                'verbose_name_plural': 'Принятый товар',
                'ordering': ['-time'],
            },
        ),
    ]
