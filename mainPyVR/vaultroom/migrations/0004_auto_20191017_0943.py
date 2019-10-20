# Generated by Django 2.2.4 on 2019-10-17 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vaultroom', '0003_auto_20191014_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='done',
            name='storage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vaultroom.Storages', verbose_name='Склад'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='control',
            name='comment',
            field=models.TextField(blank=True, max_length=500, verbose_name='Коментарий'),
        ),
        migrations.AlterField(
            model_name='control',
            name='pallet',
            field=models.IntegerField(default=0, verbose_name='Кол-во паллет'),
        ),
    ]