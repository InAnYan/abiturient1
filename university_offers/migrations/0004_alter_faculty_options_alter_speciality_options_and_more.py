# Generated by Django 5.0.3 on 2024-04-03 07:55

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_offers', '0003_alter_speciality_specialization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'faculty', 'verbose_name_plural': 'faculty.plural'},
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'verbose_name': 'speciality', 'verbose_name_plural': 'speciality.plural'},
        ),
        migrations.AlterModelOptions(
            name='universityoffer',
            options={'verbose_name': 'university_offer', 'verbose_name_plural': 'university_offer.plural'},
        ),
        migrations.AlterField(
            model_name='faculty',
            name='abbreviation',
            field=models.CharField(max_length=255, unique=True, verbose_name='generic.abbreviation'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='cipher',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='generic.cipher'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='full_name',
            field=models.CharField(max_length=255, unique=True, verbose_name='generic.full_name'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='code',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='generic.code'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='educational_program_name',
            field=models.CharField(max_length=255, verbose_name='speciality.educational_program_name'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='end_of_accreditation',
            field=models.DateField(blank=True, null=True, verbose_name='speciality.end_of_accreditation'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.faculty', verbose_name='faculty'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='name',
            field=models.CharField(max_length=255, verbose_name='generic.name'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='specialization',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='speciality.specialization'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='ects',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='university_offer.ects'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.speciality', verbose_name='speciality'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='study_begin',
            field=models.DateField(verbose_name='university_offer.study_begin'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='study_duration',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='university_offer.study_duration'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='study_form',
            field=models.PositiveIntegerField(choices=[(1, 'university_offer.study_form.day'), (2, 'university_offer.study_form.over_distance'), (3, 'university_offer.study_form.evening')], verbose_name='university_offer.study_form'),
        ),
        migrations.AlterField(
            model_name='universityoffer',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'university_offer.type.budget'), (2, 'university_offer.type.contract')], verbose_name='university_offer.type'),
        ),
    ]