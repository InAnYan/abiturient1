# Generated by Django 5.0.3 on 2024-04-22 09:12

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0001_initial'),
        ('university_offers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='generic.created_at')),
                ('payment_type', models.IntegerField(choices=[(1, 'accepting_offers.payment_type.governmental'), (2, 'accepting_offers.payment_type.town'), (3, 'accepting_offers.payment_type.private'), (4, 'accepting_offers.payment_type.privileged')], verbose_name='accepting_offers.payment_type')),
                ('payment_frequency', models.IntegerField(blank=True, choices=[(1, 'accepting_offers.payment_frequency.every_semester'), (2, 'accepting_offers.payment_frequency.every_year'), (3, 'accepting_offers.payment_frequency.every_month'), (4, 'accepting_offers.payment_frequency.full')], null=True, verbose_name='accepting_offers.payment_frequency')),
                ('accepted_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='accepting_offers.accepted_year')),
                ('abiturient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='persons.person', verbose_name='abiturient')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university_offers.universityoffer', verbose_name='university_offer')),
            ],
            options={
                'verbose_name': 'accepted_offer',
                'verbose_name_plural': 'accepted_offer.plural',
            },
        ),
    ]
