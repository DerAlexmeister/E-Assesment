# Generated by Django 4.0.4 on 2022-06-19 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0011_octastatement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qawset',
            name='Categorie',
        ),
        migrations.AddField(
            model_name='qawset',
            name='ItemType',
            field=models.CharField(choices=[('None', 'None'), ('MultipleChoice', 'MultipleChoice'), ('SingleChoice', 'SingleChoice'), ('ClozeText', 'ClozeText'), ('TruthTable', 'TruthTable'), ('Calculus', 'Calculus')], default='None', max_length=24),
        ),
        migrations.AddField(
            model_name='qawset',
            name='NameID',
            field=models.CharField(default=None, max_length=1024, null=True, unique=True),
        ),
    ]
