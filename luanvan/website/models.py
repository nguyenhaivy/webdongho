
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.

class User(AbstractUser):
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Quản lý tài khoản Đăng Nhập"
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('username').blank = False
    AbstractUser._meta.get_field('password').blank = False
    AbstractUser._meta.get_field('password').blank = False

    user_name = models.CharField('Tên khách hàng',max_length=255)
    user_phone = models.IntegerField('Số điện thoại khách hàng', blank=True, null=True)
    user_address = models.CharField('Địa chỉ khách hàng', max_length= 255, blank= True, null=True)
    user_birthday = models.DateField('Ngày sinh của khách', blank=True, null= True)
    user_avatar = models.ImageField(upload_to='user_image', default="user_image/user_empty.png", null=True,blank=True)
    update_time = models.DateTimeField(auto_now=True)
    role = models.CharField('Vai trò tài khoản',max_length= 20, blank= True, null=True,default='User')

class Suplier:
	class Meta:
		ordering = ["suplier_id"]
		verbose_name_plural = "Nhà cung cấp"
	suplier_id = models.AutoField(primary_key=True)
	suplier_name = models.CharField('Tên nhà cung cấp', max_length=255)
	url = models.CharField('Đường dẫn',max_length=100, null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
	logo = models.ImageField('Ảnh logo',upload_to='Suplier_image',null=True,blank=True)
	def __str__(self):
		return str(self.suplier_name)

class Post(models.Model):
	class Meta:
		ordering = ["post_id"]
		verbose_name_plural = "Bài đăng"
	post_id = models.AutoField(primary_key= True)
	title = models.CharField('Tiêu đề',max_length=255,null=False,blank=False)
	content = models.TextField('Nội dung', max_length=255,null = False, blank = False)
	post_date = models.DateField('Ngày đăng', auto_now=True)
	image = models.ImageField('Hình bài đăng',upload_to='Post_image',null=True,blank=True)
	def __str__(self):
		return str(self.title)

class Categories(models.Model):
    class Meta:
        ordering = ["categories_id"]
        verbose_name_plural = "Danh Mục"
    
    categories_id = models.AutoField(primary_key=True)
    categories_name = models.CharField('Tên danh mục', max_length=100, null=True, blank=True)
    url = models.CharField('Đường dẫn', max_length=100, null=True, blank=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    update_time = models.DateTimeField('Thời gian cập nhật', auto_now=True)
    
    def __str__(self):
        return str(self.categories_name)


class Promotions(models.Model):
    class Meta:
        ordering = ["promotions_id"]
        verbose_name_plural = "Phiếu Giảm Giá"
    promotions_id = models.AutoField(primary_key=True)
    promotions_code = models.IntegerField('Mã giảm giá', null=True, blank=True)
    promotions_name = models.CharField('Têm mã giảm giá', null= True, blank= True)
    promotions_discount = models.IntegerField('gía trị giảm', null = False,blank = False)
    promotions_discount_percent = models.IntegerField('Phần trăm giảm giá',null = False,blank = False)
    amount = models.IntegerField('Số lượng', null=True, blank = False)
    start_time = models.DateTimeField('Thời gian tồn tại đến ngày nào')
    end_time = models.DateTimeField('Thời gian tồn tại đến ngày nào')
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    update_time = models.DateTimeField('Thời gian cập nhật', auto_now=True)
    def __str__(self):
        return str(self.promotions_code)
	

class Trademark(models.Model):
	class Meta:
		ordering = ["trademark_id"]
		verbose_name_plural = "Thương hiệu đồng hồ"
	trademark_id = models.AutoField(primary_key=True)
	avatar = models.ImageField('Ảnh đại diện',upload_to='Trademark_image',null=True,blank=True)
	trademark_name = models.CharField('Tên thương hiệu',max_length=100, null=True, blank=True)
	url = models.CharField('Đường dẫn',max_length=100, null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

	def __str__(self):	
		return str(self.trademark_name)
	
class Price_limit(models.Model):
	class Meta:
		ordering = ["price_id"]
		verbose_name_plural = "Mức giá đồng hồ"
	price_id = models.AutoField(primary_key=True)
	price_limit_name = models.CharField('Mức giá',max_length=100, null=True, blank=True)
	url = models.CharField('Đường dẫn',max_length=100, null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

	def __str__(self):	
		return str(self.price_limit_name)

class Machine_type(models.Model):
	class Meta:
		ordering = ["machine_type_id"]
		verbose_name_plural = "Loại máy đồng hồ"

	machine_type_id = models.AutoField(primary_key=True)
	machine_type_name = models.CharField('Tên Loại máy',max_length=100, null=True, blank=True)
	url = models.CharField('Đường dẫn',max_length=100, null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

	def __str__(self):	
		return str(self.machine_type_name)


class Wire_material(models.Model):
    class Meta:
        ordering = ["wire_material_id"]
        verbose_name_plural = "Chất liệu dây"

    wire_material_id = models.AutoField(primary_key=True)
    wire_material_name = models.CharField('Tên Chất liệu dây', max_length=100, null=True, blank=True)
    url = models.CharField('Đường dẫn', max_length=100, null=True, blank=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    update_time = models.DateTimeField('Thời gian cập nhật', auto_now=True)

    def __str__(self):
        return str(self.wire_material_name)
	
class Style(models.Model):
	class Meta:
		ordering = ["style_id"]
		verbose_name_plural = "Phong cách đồng hồ"

	style_id = models.AutoField(primary_key=True)
	style_name = models.CharField('Tên Phong cách',max_length=100, null=True, blank=True)
	url = models.CharField('Đường dẫn',max_length=100, null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)

	def __str__(self):	
		return str(self.name)

class Clock(models.Model):
    class Meta:
        ordering = ["clock_id"]
        verbose_name_plural = "Sản phẩm đồng hồ"
    
    clock_id = models.AutoField(primary_key=True)
    clock_name = models.CharField('Tên đồng hồ', max_length=255)  # Added max_length as it's required for CharField
    describe = models.CharField('Mô tả',max_length=255, null=True, blank=True)
    
    categories = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='clock_categories')
    trademark = models.ForeignKey('Trademark', on_delete=models.CASCADE, related_name='clock_trademark')
    price_limit = models.ForeignKey('Price_limit', on_delete=models.CASCADE, related_name='clock_price_limit')
    machine_type = models.ForeignKey('Machine_type', on_delete=models.CASCADE, related_name='clock_machine_type')
    wire_material = models.ForeignKey('Wire_material', on_delete=models.CASCADE, related_name='clock_wire_material')
    
    price = models.IntegerField('Giá sản phẩm', null=True, blank=True)
    quantity = models.CharField('Số lượng hiện có', max_length=255, null=True, blank=True)
    sex = models.CharField('Giới tính', max_length=255, null=True, blank=True)
    designs = models.CharField('Kiểu dáng', max_length=255, null=True, blank=True)
    glass_surface = models.CharField('Mặt kính', max_length=255, null=True, blank=True)
    diameter = models.CharField('Đường kính', max_length=255, null=True, blank=True)
    face_color = models.CharField('Màu mặt', max_length=255, null=True, blank=True)
    shell_material = models.CharField('Chất liệu vỏ', max_length=255, null=True, blank=True)
    water_resistance = models.CharField('Độ chịu nước', max_length=255, null=True, blank=True)
    other_function = models.CharField('Tính năng khác', max_length=255, null=True, blank=True)
    brand_origin = models.CharField('Xuất sứ thương hiệu', max_length=255, null=True, blank=True)
    warranty_genuine = models.CharField('Bảo hành chính hãng', max_length=255, null=True, blank=True)
    percent_discount = models.IntegerField('Phần trăm giảm giá (%)', default=10, null=True, blank=True)
    price_has_decreased = models.IntegerField('Giá sau khi giảm', default=10, null=True, blank=True)
    # installment_percent = models.IntegerField('Phần trăm trả góp', default=0, null=True, blank=True)
    url = models.CharField('Đường dẫn', max_length=255, null=True, blank=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.clock_name)
	
class MediaImage(models.Model):
	class Meta:
		ordering = ["image_id"]
		verbose_name_plural = "Hình ảnh"
	image_id = models.AutoField(primary_key=True)
	image= models.ImageField('Ảnh ',upload_to='media/images',null=True,blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
	belong_clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name='list_image_clock')

class MediaVideo(models.Model):
	class Meta:
		ordering = ["video_id"]
		verbose_name_plural = "Video"
	video_id = models.AutoField(primary_key=True)
	video = models.FileField('Video', upload_to='media/videos', null=True, blank=True)
	creation_time = models.DateTimeField('Thời gian tạo',auto_now_add=True)
	update_time = models.DateTimeField('Thời gian cập nhật',auto_now=True)
	belong_clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name='list_video_clock')
	
class Comment(models.Model):
	class Meta:
		ordering = ["comment_id"]
		verbose_name_plural = "Bình luận"
	comment_id = models.AutoField(primary_key=True)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Commnet_User')
	clock_id = models.ForeignKey(Clock, on_delete=models.CASCADE, related_name='Comment_Clock')
	cmt = models.CharField('Bình Luận',max_length=255)
	rating = models.IntegerField('Điểm số', null=True, blank=True)
	def __str__(self):
		return str(self.user_name)

class Order(models.Model):
    class Meta:
        ordering = ["order_id"]
        verbose_name_plural = "Đơn Hàng"
    
    STATUS_CHOICES1 = [
        ('Chờ Xác nhận', 'Chờ Xác nhận'),
        ('Đã xác nhận', 'Đã xác nhận'),
        ('Đang giao hàng', 'Đang giao hàng'),
        ('Đã giao hàng', 'Đã giao hàng'),
    ]
    
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_customer')
    order_id = models.AutoField(primary_key=True)
    code = models.CharField('Mã đơn hàng', max_length=255)
    name = models.CharField('Tên khách hàng', max_length=255)
    promotion = models.ForeignKey(Promotions, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_promotions')
    phone = models.IntegerField('Số điện thoại khách hàng', blank=True, null=True)
    address = models.CharField('Địa chỉ khách hàng', max_length=255, blank=True, null=True)
    note = models.CharField('Ghi chú', max_length=255)
    total_amount = models.IntegerField('Tổng số lượng sản phẩm', default=1, null=False, blank=False)
    total_pay = models.IntegerField('Tổng tiền thanh toán', null=True, blank=True)
    total_price = models.IntegerField('đơn giá', null=True, blank=True)
    status = models.CharField('Trạng thái đơn hàng', default="Chờ Xác nhận", max_length=100, choices=STATUS_CHOICES1, null=True, blank=True)
    payment_type = models.CharField('Loại giao hàng', max_length=100, null=True, blank=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    

class Orderdetails(models.Model):
    class Meta:
        ordering = ["orderdetails_id"]
        verbose_name_plural = "Các mặt hàng trong đơn hàng"
    
    orderdetails_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="orderdetails")
    clock = models.ForeignKey('Clock', on_delete=models.CASCADE, related_name="clockdetails")
    quantity = models.IntegerField('Số lượng', blank=True, null=True)
    total_money = models.IntegerField('Thành tiền', blank=True, null=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    
class Installment(models.Model):
    class Meta:
        ordering = ["installment_id"]
        verbose_name_plural = "Thông tin trả góp theo sản phẩm"
    installment_id = models.AutoField(primary_key=True)
    clock_id = models.ForeignKey(Clock,on_delete=models.CASCADE, related_name="Installment_Clock")
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="Installment_User")
    installment_code = models.CharField('Mã Đơn hàng trả góp',max_length=255, blank= True, null=True)
    amount_settled = models.IntegerField('Số tiền tất toán', blank= True, null=True)
    down_payment_discount = models.IntegerField('Phần trăm trả trước (%)', default=30, null=True, blank=True)
    number_of_payments = models.IntegerField('Số kỳ trả góp', null=True, blank=True)
    amount = models.IntegerField('Giá mua trả góp', null=True, blank=True)
    down_payment = models.IntegerField('Số tiền trả trước', null=True, blank=True)
    amount_of_payment = models.IntegerField('Số tiền trong 1 kỳ', null=True, blank=True)
    total_amount = models.IntegerField('Tổng tiền phải trả', null=True, blank=True)
    settled = models.BooleanField('Tất toán chưa',default=False)
    user_name = models.CharField('Tên khách hàng',max_length=255,null=True, blank=True)
    user_sex = models.CharField('Giới tính khách hàng',max_length=255,null=True, blank=True)
    user_phone = models.CharField('Số điện thoại khách hàng', blank=True, null=True)
    user_address = models.CharField('Địa chỉ khách hàng', max_length= 255, blank= True, null=True)
    user_IDcard = models.CharField('số căn cước công cân', blank=True, null=True)
    user_phone_family_1 = models.CharField('Số điện thoại người thân 1', blank=True, null=True)
    user_phone_family_2 = models.CharField('Số điện thoại người thân 2', blank=True, null=True)
    user_gh = models.CharField('Loại Giao Hàng', blank=True, null=True)
    status = models.CharField('Trang thái đơn trả góp',default="Chờ Xác nhận",max_length=100, null=True, blank=True)
    accept_time = models.DateTimeField('Thời gian duyệt', blank=True, null=True)
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    def __str__(self):
        return str(self.installment_id)
	


class Installment_Period(models.Model):
    period_code = models.CharField('Mã Thanh Toán',max_length=255, blank= True, null=True)
    period_name = models.CharField('Tên kỳ trả góp',max_length=255, blank= True, null=True)
    period_amount = models.IntegerField('Số tiền trong 1 kỳ', null=True, blank=True)
    period_day = models.DateTimeField('Thời gian trả', blank= True, null=True)
    period = models.BooleanField('Đã trả chưa',default=False)
    installment_id = models.ForeignKey(Installment,on_delete=models.CASCADE, related_name="List_period_installment")
    creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)
    
	
class Image_Installment(models.Model):
	image = models.ImageField('Ảnh trả góp',upload_to='Image_Installment',null=True,blank=True)
	installment_id = models.ForeignKey(Installment,on_delete=models.CASCADE, related_name="List_image_installment")
	creation_time = models.DateTimeField('Thời gian tạo', auto_now_add=True)