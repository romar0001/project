# Generated by Django 4.1 on 2022-12-03 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='type',
            field=models.CharField(choices=[('SALESEXECUTIVE', 'Sales Executive'), ('TECHNICIAN', 'Tecnician')], default='SALESEXECUTIVE', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(max_length=255),
        ),
    ]
