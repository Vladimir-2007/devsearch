# Generated by Django 3.2.4 on 2023-07-30 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230730_1339'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skill',
            new_name='Skills',
        ),
    ]