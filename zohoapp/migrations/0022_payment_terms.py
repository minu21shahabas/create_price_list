# Generated by Django 4.1.4 on 2023-05-09 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0021_alter_estimates_cgst_alter_estimates_sgst'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment_terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Terms', models.CharField(blank=True, max_length=100, null=True)),
                ('Days', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]