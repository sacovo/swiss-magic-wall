# Generated by Django 3.1.4 on 2020-12-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0005_votationdate_latest_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='votation',
            name='related',
            field=models.ManyToManyField(blank=True,
                                         related_name='_votation_related_+',
                                         to='votes.Votation'),
        ),
    ]
