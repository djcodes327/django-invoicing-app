# Generated by Django 4.2.6 on 2023-10-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
