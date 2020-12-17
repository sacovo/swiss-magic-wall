# Generated by Django 3.1.4 on 2020-12-06 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("geo", "0001_initial"),
        ("votes", "0001_initial"),
        ("predict", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(model_name="votingmodel",
                               old_name="projection",
                               new_name="yes_projection"),
        migrations.AddField(
            model_name="votingmodel",
            name="participation_projection",
            field=models.FileField(blank=True,
                                   null=True,
                                   upload_to="",
                                   verbose_name="projections/"),
        ),
        migrations.AlterField(
            model_name="votingmodel",
            name="model_votations",
            field=models.ManyToManyField(
                blank=True,
                related_name="_votingmodel_model_votations_+",
                to="votes.Votation",
            ),
        ),
        migrations.CreateModel(
            name="LatestResult",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("yes_percent", models.FloatField()),
                ("participation", models.FloatField()),
                ("yes_absolute", models.IntegerField()),
                ("no_absolute", models.IntegerField()),
                ("is_final", models.BooleanField()),
                ("timestamp", models.DateTimeField(auto_now=True)),
                (
                    "gemeinde",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                      to="geo.gemeinde"),
                ),
                (
                    "votation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                      to="votes.votation"),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="latestresult",
            constraint=models.UniqueConstraint(fields=("gemeinde", "votation"),
                                               name="unique_gemeinde_votation"),
        ),
    ]
