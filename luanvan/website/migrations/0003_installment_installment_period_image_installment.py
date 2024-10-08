# Generated by Django 4.2.13 on 2024-07-23 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_delete_installment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('installment_id', models.AutoField(primary_key=True, serialize=False)),
                ('down_payment_discount', models.IntegerField(blank=True, default=30, null=True, verbose_name='Phần trăm trả trước (%)')),
                ('number_of_payments', models.IntegerField(blank=True, null=True, verbose_name='Số kỳ trả góp')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='Giá mua trả góp')),
                ('down_payment', models.IntegerField(blank=True, null=True, verbose_name='Số tiền trả trước')),
                ('amount_of_payment', models.IntegerField(blank=True, null=True, verbose_name='Số tiền trong 1 kỳ')),
                ('total_amount', models.IntegerField(blank=True, null=True, verbose_name='Tổng tiền phải trả')),
                ('settled', models.BooleanField(default=False, verbose_name='Tất toán chưa')),
                ('user_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tên khách hàng')),
                ('user_sex', models.CharField(blank=True, max_length=255, null=True, verbose_name='Giới tính khách hàng')),
                ('user_phone', models.CharField(blank=True, null=True, verbose_name='Số điện thoại khách hàng')),
                ('user_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Địa chỉ khách hàng')),
                ('user_IDcard', models.CharField(blank=True, null=True, verbose_name='số căn cước công cân')),
                ('user_phone_family_1', models.CharField(blank=True, null=True, verbose_name='Số điện thoại người thân 1')),
                ('user_phone_family_2', models.CharField(blank=True, null=True, verbose_name='Số điện thoại người thân 2')),
                ('user_gh', models.CharField(blank=True, null=True, verbose_name='Loại Giao Hàng')),
                ('status', models.CharField(blank=True, choices=[('Chờ xác nhận', 'Chờ xác nhận'), ('Đang chạy', 'Đang chạy'), ('Đã tất toán', 'Đã tất toán'), ('Thanh toán trễ', 'Thanh toán trễ')], default='Chờ Xác nhận', max_length=100, null=True, verbose_name='Trang thái đơn trả góp')),
                ('accept_time', models.DateTimeField(blank=True, null=True, verbose_name='Thời gian duyệt')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')),
                ('clock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Installment_Clock', to='website.clock')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Installment_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Thông tin trả góp theo sản phẩm',
                'ordering': ['installment_id'],
            },
        ),
        migrations.CreateModel(
            name='Installment_Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tên kỳ trả góp')),
                ('period_amount', models.IntegerField(blank=True, null=True, verbose_name='Số tiền trong 1 kỳ')),
                ('period_day', models.DateTimeField(blank=True, null=True, verbose_name='Thời gian trả')),
                ('period', models.BooleanField(default=False, verbose_name='Đã trả chưa')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')),
                ('period_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='List_period_installment', to='website.installment')),
            ],
        ),
        migrations.CreateModel(
            name='Image_Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Image_Installment', verbose_name='Ảnh trả góp')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo')),
                ('installment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='List_image_installment', to='website.installment')),
            ],
        ),
    ]
