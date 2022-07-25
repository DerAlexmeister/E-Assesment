# Generated by Django 4.0.4 on 2022-07-21 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0037_merge_20220721_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='gatesanswer',
            name='UserID',
            field=models.CharField(default='None', max_length=1024),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='Duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='singlechoiceuseranswer',
            name='Set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EAss.qawset'),
        ),
        migrations.AlterField(
            model_name='qawset',
            name='ItemType',
            field=models.CharField(choices=[('None', 'None'), ('MultipleChoice', 'MultipleChoice'), ('SingleChoice', 'SingleChoice'), ('ClozeText', 'ClozeText'), ('TruthTable', 'TruthTable'), ('Calculus', 'Calculus'), ('Assembler', 'Assembler'), ('Gates', 'Gates')], default='None', max_length=24),
        ),
    ]