# Generated by Django 3.2.11 on 2022-02-10 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название принтера')),
                ('api_key', models.CharField(blank=True, max_length=100, unique=True, verbose_name='API ключ')),
                ('check_type', models.CharField(choices=[('kitchen', 'Кухня'), ('client', 'Клиент')], max_length=64, verbose_name='Тип чека')),
                ('point', models.PositiveIntegerField(verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Принтер',
                'verbose_name_plural': 'Принтеры',
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('kitchen', 'Кухня'), ('client', 'Клиент')], max_length=64, verbose_name='Тип чека')),
                ('order', models.JSONField(verbose_name='Информация о заказе')),
                ('status', models.CharField(choices=[('new', 'Новый'), ('rendered', 'Полученный'), ('printed', 'Напечатанный')], default='new', max_length=64, verbose_name='Статус чека')),
                ('pdf_file', models.FileField(blank=True, max_length=254, upload_to='pdf')),
                ('printer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chequeapp.printer', verbose_name='Принтер')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
            },
        ),
    ]
