# Generated by Django 4.2.6 on 2023-10-14 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0006_alter_usersettings_options_delete_invoicelineitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='paymentTerms',
            field=models.CharField(blank=True, choices=[('7 Days', '7 Days'), ('15 Days', '15 Days'), ('30 Days', '30 Days'), ('45 Days', '45 Days'), ('60 Days', '60 Days'), ('90 Days', '90 Days')], max_length=20, null=True),
        ),
    ]
