# Generated by Django 4.0.4 on 2022-07-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0039_calculussingleuseranswer_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='Hint',
            field=models.TextField(default='no hint'),
        ),
        migrations.AddField(
            model_name='wrongstatements',
            name='Hint',
            field=models.TextField(default='no hint'),
        ),
    ]