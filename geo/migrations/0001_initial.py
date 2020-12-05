# Generated by Django 3.1.4 on 2020-12-05 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Kanton",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("geo_id", models.IntegerField(primary_key=True,
                                               serialize=False)),
                ("standesstimme", models.FloatField(default=1.0)),
            ],
            options={
                "ordering": ["geo_id"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Gemeinde",
            fields=[
                ("name", models.CharField(max_length=100)),
                ("geo_id", models.IntegerField(primary_key=True,
                                               serialize=False)),
                ("voters", models.IntegerField()),
                (
                    "kanton",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="geo.kanton"),
                ),
            ],
            options={
                "ordering": ["geo_id"],
                "abstract": False,
            },
        ),
    ]