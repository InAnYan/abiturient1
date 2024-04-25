# Generated by Django 5.0.4 on 2024-04-24 06:54

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
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_serie', models.CharField(blank=True, max_length=2, null=True, verbose_name='persons.passport_serie')),
                ('passport_number', models.IntegerField(verbose_name='persons.passport_number')),
                ('passport_who_give', models.TextField(verbose_name='persons.passport_who_give')),
                ('passport_when_given', models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date.today)], verbose_name='persons.passport_when_given')),
                ('inn', models.IntegerField(verbose_name='persons.inn')),
            ],
            options={
                'verbose_name': 'persons.passport',
                'verbose_name_plural': 'persons.passport.plural',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, verbose_name='generic.last_name')),
                ('first_name', models.CharField(max_length=255, verbose_name='generic.first_name')),
                ('patronymic', models.CharField(max_length=255, verbose_name='generic.patronymic')),
                ('phone', models.IntegerField(verbose_name='generic.telephone')),
                ('email', models.EmailField(max_length=254, verbose_name='generic.email')),
                ('living_address', models.TextField(verbose_name='abiturient.living_address')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='persons.person', verbose_name='persons.parent')),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='persons.passport', verbose_name='persons.passport')),
            ],
            options={
                'verbose_name': 'abiturient',
                'verbose_name_plural': 'abiturient.plural',
            },
        ),
    ]
