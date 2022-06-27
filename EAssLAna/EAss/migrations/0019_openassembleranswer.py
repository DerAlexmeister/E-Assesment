# Generated by Django 4.0.4 on 2022-06-26 12:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0018_alter_qawset_itemtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenAssemblerAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField()),
                ('Answer', models.TextField()),
                ('Solved', models.DateTimeField(default=django.utils.timezone.now)),
                ('Correct', models.BooleanField()),
            ],
        ),
    ]
