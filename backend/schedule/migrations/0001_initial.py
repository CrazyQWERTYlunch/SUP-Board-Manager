# Generated by Django 5.0.1 on 2024-02-20 21:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_seats', models.PositiveSmallIntegerField(verbose_name='Количество мест')),
                ('remaining_seats', models.PositiveIntegerField(verbose_name='Осталось мест')),
                ('date', models.DateField(verbose_name='Дата')),
                ('start', models.TimeField(blank=True, null=True, verbose_name='Начало')),
                ('end', models.TimeField(blank=True, null=True, verbose_name='Конец')),
                ('status', models.CharField(default='Предстоит', max_length=50, verbose_name='Статус события')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.route', verbose_name='Маршрут')),
            ],
            options={
                'verbose_name': 'Прогулка',
                'verbose_name_plural': 'Прогулки',
                'db_table': 'tblevents',
            },
        ),
    ]