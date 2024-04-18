# Generated by Django 5.0.3 on 2024-04-18 08:11

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, verbose_name='generic.last_name')),
                ('first_name', models.CharField(max_length=255, verbose_name='generic.first_name')),
                ('patronymic', models.CharField(max_length=255, verbose_name='generic.patronymic')),
                ('phone', models.PositiveIntegerField(max_length=12, validators=[django.core.validators.RegexValidator('\\d+', 'generic.only_numbers'), django.core.validators.MinLengthValidator(9)], verbose_name='generic.telephone')),
                ('email', models.EmailField(max_length=254, verbose_name='generic.email')),
                ('living_address', models.TextField(verbose_name='abiturient.living_address')),
                ('passport_serie', models.CharField(max_length=2, verbose_name='persons.passport_serie')),
                ('passport_number', models.PositiveIntegerField(max_length=9, verbose_name='persons.passport_number')),
                ('passport_who_give', models.PositiveIntegerField(max_length=4, verbose_name='persons.passport_who_give')),
                ('passport_when_given', models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)], verbose_name='persons.passport_when_given')),
                ('inn', models.PositiveIntegerField(max_length=12, verbose_name='persons.inn')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='persons.person')),
            ],
            options={
                'verbose_name': 'abiturient',
                'verbose_name_plural': 'abiturient.plural',
            },
        ),
    ]
