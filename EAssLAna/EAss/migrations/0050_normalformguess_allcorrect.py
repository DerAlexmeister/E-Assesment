# Generated by Django 4.0.4 on 2022-07-25 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0049_merge_20220725_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='normalformguess',
            name='AllCorrect',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
