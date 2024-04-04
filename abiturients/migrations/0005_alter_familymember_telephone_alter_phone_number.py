# Generated by Django 5.0.3 on 2024-04-04 07:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abiturients', '0004_alter_abiturient_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='telephone',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator('\\d+', 'generic.only_numbers')], verbose_name='generic.telephone'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(max_length=9, validators=[django.core.validators.RegexValidator('\\d+', 'generic.only_numbers')], verbose_name='phone.number'),
        ),
    ]
