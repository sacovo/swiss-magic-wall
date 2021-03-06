# Generated by Django 3.1.4 on 2020-12-18 09:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('predict', '0001_initial'),
        ('votes', '0001_initial'),
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingmodel',
            name='model_votations',
            field=models.ManyToManyField(blank=True,
                                         related_name='_votingmodel_model_votations_+',
                                         to='votes.Votation',
                                         verbose_name='model votations'),
        ),
        migrations.AddField(
            model_name='votingmodel',
            name='votation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                       related_name='projection',
                                       to='votes.votation',
                                       verbose_name='votation'),
        ),
        migrations.AddField(
            model_name='result',
            name='gemeinde',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='geo.gemeinde',
                                    verbose_name='commune'),
        ),
        migrations.AddField(
            model_name='result',
            name='timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='predict.timestamp'),
        ),
        migrations.AddField(
            model_name='result',
            name='votation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='votes.votation',
                                    verbose_name='votation'),
        ),
        migrations.AddField(
            model_name='latestresult',
            name='gemeinde',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='geo.gemeinde',
                                    verbose_name='commune'),
        ),
        migrations.AddField(
            model_name='latestresult',
            name='votation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    to='votes.votation',
                                    verbose_name='votation'),
        ),
        migrations.AddConstraint(
            model_name='latestresult',
            constraint=models.UniqueConstraint(fields=('gemeinde', 'votation'),
                                               name='unique_gemeinde_votation'),
        ),
    ]
