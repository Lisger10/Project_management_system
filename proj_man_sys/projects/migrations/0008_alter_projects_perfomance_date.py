# Generated by Django 4.2.3 on 2023-07-21 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_projects_perfomance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='perfomance_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
