# Generated by Django 5.0.4 on 2024-05-23 06:30

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EducationalProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, unique=True, verbose_name='Full name')),
                ('abbreviation', models.CharField(max_length=255, unique=True, verbose_name='Abbreviation')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Accreditation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(choices=[(1, 'Bachelor'), (2, 'Master'), (3, 'PhD')], verbose_name='Educational level')),
                ('end_date', models.DateField(verbose_name='End of accreditation')),
                ('number', models.PositiveIntegerField(verbose_name='Accreditation number')),
                ('serie', models.CharField(blank=True, max_length=2, null=True, verbose_name='Accreditation serie')),
                ('type', models.PositiveIntegerField(choices=[(1, 'Speciality'), (2, 'Educational program')], verbose_name='Accreditation type')),
                ('educational_program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.educationalprogram', verbose_name='Educational program')),
            ],
            options={
                'verbose_name': 'Accreditation',
                'verbose_name_plural': 'Accreditations',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='Code')),
                ('specialization_code', models.IntegerField(blank=True, help_text='If there is a specialization, fill the specialization code and leave name to be the name of the specialization', null=True, verbose_name='Specialization code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.faculty', verbose_name='Faculty')),
            ],
            options={
                'verbose_name': 'Speciality',
                'verbose_name_plural': 'Specialities',
            },
        ),
        migrations.AddField(
            model_name='educationalprogram',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.speciality', verbose_name='Speciality'),
        ),
        migrations.CreateModel(
            name='UniversityOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_begin', models.DateField(verbose_name='Beginning of study')),
                ('study_duration', models.IntegerField(help_text='In months', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Study duration')),
                ('level', models.PositiveIntegerField(choices=[(1, 'Bachelor'), (2, 'Master'), (3, 'PhD')], verbose_name='Educational level')),
                ('basis', models.PositiveIntegerField(choices=[(1, 'CGSE'), (2, 'NFQ5'), (3, 'NFQ6 or NFQ7')], verbose_name='Basis')),
                ('type', models.PositiveIntegerField(choices=[(1, 'Budget'), (2, 'Contract')], help_text='Budget or contract', verbose_name='Offer type')),
                ('study_form', models.PositiveIntegerField(choices=[(1, 'Full-time'), (2, 'Part-time'), (3, 'Distance')], verbose_name='Study form')),
                ('ects', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='ECTS')),
                ('year1_cost', models.PositiveIntegerField(default=0, verbose_name='Year 1 cost')),
                ('year2_cost', models.PositiveIntegerField(default=0, verbose_name='Year 2 cost')),
                ('year3_cost', models.PositiveIntegerField(default=0, verbose_name='Year 3 cost')),
                ('year4_cost', models.PositiveIntegerField(default=0, verbose_name='Year 4 cost')),
                ('educational_program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.educationalprogram', verbose_name='Educational program')),
            ],
            options={
                'verbose_name': 'University offer',
                'verbose_name_plural': 'University offers',
            },
        ),
    ]
