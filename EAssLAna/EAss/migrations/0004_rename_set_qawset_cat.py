# Generated by Django 4.0.4 on 2022-06-11 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EAss', '0003_categorie_rename_length_binarystatement_maxvalue_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qawset',
            old_name='Set',
            new_name='Cat',
        ),
    ]
