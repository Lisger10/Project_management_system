# Generated by Django 4.2.3 on 2023-07-24 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_task_perfomance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Открыта', 'Открыта'), ('Закрыта', 'Закрыта')], max_length=10),
        ),
    ]
