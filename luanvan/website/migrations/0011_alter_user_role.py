# Generated by Django 4.2.13 on 2024-08-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_order_payment_type_alter_order_total_pay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, default='User', max_length=20, null=True, verbose_name='Vai trò tài khoản'),
        ),
    ]
