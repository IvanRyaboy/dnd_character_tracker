# Generated by Django 5.1 on 2024-09-19 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0005_remove_characterclass_skills_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='skills',
        ),
    ]
