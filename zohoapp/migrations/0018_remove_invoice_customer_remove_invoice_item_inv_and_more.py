# Generated by Django 4.1.4 on 2023-05-06 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0017_invoice_estimates_cgst_estimates_igst_estimates_sgst_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='invoice_item',
            name='inv',
        ),
        migrations.DeleteModel(
            name='customer',
        ),
        migrations.DeleteModel(
            name='invoice',
        ),
        migrations.DeleteModel(
            name='invoice_item',
        ),
    ]
