# Generated by Django 4.2.3 on 2023-07-17 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_projects_perfomance_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-id']},
        ),
    ]