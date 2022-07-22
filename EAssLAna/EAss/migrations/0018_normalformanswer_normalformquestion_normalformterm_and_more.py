# Generated by Django 4.0.4 on 2022-07-20 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0017_alter_normalform_assessment'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalFormAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NormalFormQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal_form', models.CharField(choices=[('conjunctive', 'conjunctive'), ('disjunctive', 'disjunctive')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NormalFormTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformanswer')),
            ],
        ),
        migrations.CreateModel(
            name='NormalFormLiteral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(max_length=20)),
                ('sign', models.BooleanField()),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformterm')),
            ],
        ),
        migrations.CreateModel(
            name='NormalFormGuess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformanswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformquestion')),
            ],
        ),
        migrations.CreateModel(
            name='NormalFormCorrection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('guess', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformguess')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one', models.SmallIntegerField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAss.normalformquestion')),
            ],
        ),
    ]