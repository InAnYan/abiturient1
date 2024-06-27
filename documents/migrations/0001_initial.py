# Generated by Django 5.0.4 on 2024-06-27 10:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('([^\\W]| )+', 'Only alphabetical characters are allowed')], verbose_name='Name')),
                ('file', models.FileField(upload_to='documents', verbose_name='File')),
                ('only_for_contract', models.BooleanField(default=False, verbose_name='Only for contract offers')),
                ('only_for_full_time', models.BooleanField(default=False, verbose_name='Only for full-time offers')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
    ]
