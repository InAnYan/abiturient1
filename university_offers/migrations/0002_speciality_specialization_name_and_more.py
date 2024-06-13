# Generated by Django 5.0.4 on 2024-06-13 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='speciality',
            name='specialization_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Specialization name'),
        ),
        migrations.AlterField(
            model_name='speciality',
            name='specialization_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='Specialization code'),
        ),
    ]