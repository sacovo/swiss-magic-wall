# Generated by Django 3.1.4 on 2020-12-18 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Kanton',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('geo_id', models.IntegerField(primary_key=True, serialize=False)),
                ('standesstimme',
                 models.FloatField(default=1.0, verbose_name='standesstimme')),
            ],
            options={
                'verbose_name': 'canton',
                'verbose_name_plural': 'cantons',
            },
        ),
        migrations.CreateModel(
            name='Gemeinde',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('geo_id', models.IntegerField(primary_key=True, serialize=False)),
                ('voters', models.IntegerField(verbose_name='eligible voters')),
                ('kanton',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='geo.kanton',
                                   verbose_name='canton')),
            ],
            options={
                'verbose_name': 'commune',
                'verbose_name_plural': 'communes',
            },
        ),
    ]
