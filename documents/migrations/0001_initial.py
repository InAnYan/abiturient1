# Generated by Django 5.0.3 on 2024-04-22 09:12

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
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('([^\\W]| )+', 'generic.only_alpha')])),
                ('file', models.FileField(upload_to='documents')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'document.plural',
            },
        ),
    ]
