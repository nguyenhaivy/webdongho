# Generated by Django 5.1 on 2024-08-13 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_installment_period_congchuoi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment_period',
            name='congchuoi',
        ),
    ]
