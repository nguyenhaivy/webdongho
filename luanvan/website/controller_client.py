from .models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator

from datetime import datetime

from django.http import HttpResponse
import requests
import time
from django.http import Http404

from django.db import models
from django.utils import timezone

import os

from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import random
import string
from django.contrib.auth import update_session_auth_hash
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import random
import string

import base64

import time
from django.http import JsonResponse

import re
import json

from django.conf import settings
from .service import *
import datetime

# Trong templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def sort_by_id(value):
    # Sắp xếp danh sách theo ID tăng dần
    return sorted(value, key=lambda x: x.id)



# Chọn ngôn ngữ//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def set_Domain():
	Domain = 'http://127.0.0.1:8000'
	return Domain

# def base_page(request):
#     if request.method == 'GET':
#         base_dir = settings.BASE_DIR
#         print('base_dir:',base_dir)
#         context = {}
#         return render(request, 'base1.html', context, status=200)
    
# Chọn ngôn ngữ//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def set_Domain():
	Domain = 'http://127.0.0.1:8000'
	return Domain

def detail_post_page(request,pk):
    if request.method == 'GET':
        context = {}
        obj = Post.objects.get(pk=pk)
        context['obj'] = obj
        return render(request, 'client/post_detail_page.html', context, status=200)

def installment_page(request,pk):
    if request.method == 'GET':
        context = {}
        obj = Clock.objects.get(pk=pk)
        context['obj'] = obj
        # Phần trăm trả góp
        list_down_payment_percent = [
            {'down_payment_percent':30,'down_payment':round((30/100)*obj.price_has_decreased)},
            {'down_payment_percent':40,'down_payment':round((40/100)*obj.price_has_decreased)},
            {'down_payment_percent':50,'down_payment':round((50/100)*obj.price_has_decreased)},
        ]
        context['list_down_payment_percent']=list_down_payment_percent
        input_payment_percent=request.GET.get('input_payment_percent')
        if not input_payment_percent:
            input_payment_percent = 30
        input_payment_month=request.GET.get('input_payment_month')
        if not input_payment_month:
            input_payment_month = 3
        context['input_detail']={'pp':int(input_payment_percent),'pm':int(input_payment_month)}
        print('context[]:',context['input_detail'])
        list_installment_detail = {}
        list_installment_detail['amount']=obj.price_has_decreased
        list_installment_detail['down_payment']=round((int(input_payment_percent)/100)*obj.price_has_decreased)
        list_installment_detail['number_of_payments']=input_payment_month
        list_installment_detail['amount_of_payment']= round((int(list_installment_detail['amount'])-int(list_installment_detail['down_payment']))/int(input_payment_month)+11000+((3/100*list_installment_detail['amount'])/int(input_payment_month)))
        list_installment_detail['total_amount']= list_installment_detail['amount_of_payment']*int(input_payment_month)+list_installment_detail['down_payment']
        list_installment_detail['Spreads'] = list_installment_detail['total_amount'] - list_installment_detail['amount']
        list_installment_detail['interest'] = list_installment_detail['amount_of_payment'] - 11000
        list_installment_detail['total'] = list_installment_detail['total_amount']
        context['list_installment_detail']=list_installment_detail
        return render(request, 'client/installment_page.html', context, status=200)

def amount_settled_page(request):
    if request.method == 'POST':
        id=request.POST.get('id_setlled')
        print('id:',id)
        obj = Installment.objects.get(pk=int(id))
        list_period_payment = Installment_Period.objects.filter(period_id = obj,period = True)
        list_period = Installment_Period.objects.filter(period_id = obj,period = False)
        total_amount_settled = 0
        for i in list_period_payment:
            total_amount_settled = total_amount_settled + int(i.period_amount)
        total_amount_not_settled = int(obj.total_amount) - total_amount_settled
        total_amount_not_settled = total_amount_not_settled - total_amount_not_settled*(3/100)
        total_amount_not_settled = total_amount_not_settled -11000*(int(len(list_period))-1)
        total_amount_not_settled = round(total_amount_not_settled)
        context={}
        context ['obj']=obj
        context ['total_amount_not_settled']=total_amount_not_settled
        print('total_amount_not_settled:',total_amount_not_settled)
        print('obj.total_amount:',obj.total_amount)
        print('total_amount_settled:',total_amount_settled)
        if total_amount_not_settled:
            obj.amount_settled = total_amount_not_settled
            obj.save()

        url = reverse('period_installment_page')  # Lấy URL của trang đích
        query_params = f"?total_amount_not_settled={total_amount_not_settled}&id={id}"
        return redirect(f"{url}{query_params}")

def period_installment_page(request):
     if request.method == 'GET':
        context = {}
        total_amount_not_settled  = request.GET.get('total_amount_not_settled')
        if total_amount_not_settled:
            context['total_amount_not_settled']=total_amount_not_settled
        id = request.GET.get('id')
        if id:
            obj= Installment.objects.get(pk=int(id))
            context['obj']=obj
        list_installment = Installment.objects.filter(user_id = request.user)
        context['list_installment']=list_installment
    
        return render(request, 'client/period_installment_page.html', context, status=200)

def generate_random_uppercase_code(length=8):
    random_code = ''.join(random.choices(string.ascii_uppercase, k=length))
    return random_code




def payment_page(request):
    if request.method == 'POST':
        pk  = request.POST.get('input_id')
        print('pk:',pk)
        obj = Installment_Period.objects.get(pk = int(pk))
        code = obj.period_code
        amount = obj.period_amount
        print('code:',code)
        dtt = False
        # Lấy ngày hiện tại
        from datetime import datetime
        # Lấy ngày hiện tại
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Cập nhật URL với ngày hiện tại
        url = f"https://oauth.casso.vn/v2/transactions?fromDate={current_date}"
        print('url:',url)
        payload = {}
        headers = {
        'Authorization': 'Apikey AK_CS.6d7c46c04a8d11ef9068f9e08e26656f.1FzoN9iG5m3HYzV82fC8vVR9NnNzBBLZTrXLy0P1iXfbnZjFdfT77Rqa4VPQBr5Lbbt2vsPd',
        }
        for i in range(60):
            response = requests.request("GET", url, headers=headers, data=payload)
            response = response.json()
            for j in response['data']['records']:
                # Chuỗi đầu vào
                input_string = j['description']
                # Tách chuỗi thành danh sách các phần tử ngăn cách nhau bằng khoảng trống
                result_list = input_string.split()
                result_list = result_list[2].split('-')
                result_list  = result_list[0]
                # In ra danh sách kết quả
                print('result_list:',result_list)
                if code == result_list and int(j['amount'])== amount:
                    dtt = True
                    print('dtt:',dtt)
                    break
            if dtt:
                break
            time.sleep(3)
        if dtt:
            obj.period = True
            obj.save()
        

        return redirect('period_installment_page')
def Settled_payment_page(request):
    if request.method == 'POST':
        pk  = request.POST.get('input_id_installment')
        print('pk:',pk)
        obj = Installment.objects.get(pk = int(pk))
        code = obj.installment_code
        amount = obj.amount_settled
        dtt = False
        # Lấy ngày hiện tại
        from datetime import datetime
        # Lấy ngày hiện tại
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Cập nhật URL với ngày hiện tại
        url = f"https://oauth.casso.vn/v2/transactions?fromDate={current_date}"
        print('url:',url)
        payload = {}
        headers = {
        'Authorization': 'Apikey AK_CS.6d7c46c04a8d11ef9068f9e08e26656f.1FzoN9iG5m3HYzV82fC8vVR9NnNzBBLZTrXLy0P1iXfbnZjFdfT77Rqa4VPQBr5Lbbt2vsPd',
        }
        for i in range(60):
            response = requests.request("GET", url, headers=headers, data=payload)
            response = response.json()
            for j in response['data']['records']:
                # Chuỗi đầu vào
                input_string = j['description']
                # Tách chuỗi thành danh sách các phần tử ngăn cách nhau bằng khoảng trống
                result_list = input_string.split()
                result_list = result_list[2].split('-')
                result_list  = result_list[0]
                # In ra danh sách kết quả
                print('result_list:',result_list)
                if code == result_list and int(j['amount'])== amount:
                    dtt = True
                    print('dtt:',dtt)
                    break
            if dtt:
                break
            time.sleep(3)
        if dtt:
            list_preriod_not_pay = Installment_Period.objects.filter(period_id=obj,period=False)
            for k in list_preriod_not_pay:
                k.period = True
                k.save()
            obj.settled = True
            obj.save()
        

        return redirect('period_installment_page')

def order_installment_page(request,pk):
     if request.method == 'GET':
        context = {}
        obj = Clock.objects.get(pk=pk)
        context['obj'] = obj
        list_installment_detail = {}
        list_installment_detail['amount']=request.GET.get('amount')
        list_installment_detail['down_payment']=request.GET.get('down_payment')
        list_installment_detail['amount_of_payment']=request.GET.get('amount_of_payment')
        list_installment_detail['total']=request.GET.get('total')
        list_installment_detail['pp']=request.GET.get('pp')
        list_installment_detail['pm']=request.GET.get('pm')
        context['list_installment_detail']=list_installment_detail
        return render(request, 'client/order_installment_page.html', context, status=200)
     if request.method =='POST':
        amount = request.POST.get('amount')
        down_payment = request.POST.get('down_payment')
        amount_of_payment = request.POST.get('amount_of_payment')
        total = request.POST.get('total')
        pp = request.POST.get('pp')
        pm =  request.POST.get('pm')
        sex =  request.POST.get('sex')
        user_name = request.POST.get('user_name')
        user_phone_1 = request.POST.get('user_phone_1')
        user_phone_2 = request.POST.get('user_phone_2')
        user_phone = request.POST.get('user_phone')
        user_cccd = request.POST.get('user_cccd')
        user_image_cccd = request.FILES.getlist('user_image_cccd')
        gh = request.POST.get('gh')
        address = request.POST.get('address')

        obj_clock = Clock.objects.get(pk=pk)

        def generate_random_uppercase_code(length=9):
            # Tạo một chuỗi ngẫu nhiên gồm các chữ cái in hoa với độ dài xác định
            random_code = ''.join(random.choices(string.ascii_uppercase, k=length))
            return random_code

        if user_phone_1 != user_phone_2 and user_phone_1 != user_phone and user_phone_2 != user_phone:
            obj_installment = Installment.objects.create(
                                                clock_id = obj_clock,
                                                user_id = request.user,
                                                down_payment_discount = pp,
                                                number_of_payments = pm,
                                                amount = amount,
                                                down_payment =  down_payment,
                                                amount_of_payment = amount_of_payment,
                                                total_amount = total,
                                                user_name = user_name,
                                                user_phone = user_phone,
                                                user_phone_family_1 = user_phone_1,
                                                user_phone_family_2 = user_phone_2,
                                                user_IDcard = user_cccd,
                                                user_sex = sex,
                                                user_address = address,
                                                user_gh = gh,
                                                installment_code = generate_random_uppercase_code()
                                            )
            for i in user_image_cccd:
                Image_Installment.objects.create(image=i,installment_id=obj_installment)
            return redirect('period_installment_page')
        else:
            messages.error(request, 'Các số điện thoại không được phép trùng nhau !')
            return redirect('order_installment_page',pk=obj.clock_id)


def home_page(request):
    if request.method == 'GET':
        list_post = Post.objects.all()
        context = {}
        context['list_post'] = list_post
        search = request.GET.get('search')
        context['search'] = search
        if search:
            list_clock = Clock.objects.filter(Q(clock_name__icontains=search) | Q(describe__icontains=search))
        else:
            context['search'] = ''
            list_clock = Clock.objects.all()
        context['list_clock'] = list_clock
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material
        list_categories = Categories.objects.all()
        context['list_categories'] = list_categories
        return render(request, 'client/home_page.html', context, status=200)

def home(request):
    if request.method == 'GET':
        list_post = Post.objects.all() 
        context = {}
        context['list_post'] = list_post
        search = request.GET.get('search')
        context['search'] = search
        if search:
            list_clock = Clock.objects.filter(Q(clock_name__icontains=search) | Q(describe__icontains=search))
        else:
            context['search'] = ''
            list_clock = Clock.objects.all()
        context['list_clock'] = list_clock
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material
        list_categories = Categories.objects.all()
        context['list_categories'] = list_categories
       
        return render(request, 'client/home.html',context, status=200)

def filter_clock(request):
    if request.method == 'GET':
        context = {}
        key_trademark=request.GET.get('key_trademark')
        key_price_limit= request.GET.get('key_price_limit')
        key_machine_type= request.GET.get('key_machine_type')
        key_wire_material= request.GET.get('key_wire_material')
        key_categories= request.GET.get('key_categories')
        # key_sex= request.GET.get('key_sex')

        key_filter = {}
        context['key_filter'] = key_filter

        query = {}
        if key_trademark:
            trademark = Trademark.objects.get(trademark_name=key_trademark)
            query['trademark'] = trademark
            key_filter['key_trademark']=key_trademark
        if key_price_limit:
            price_limit = Price_limit.objects.get(price_limit_name = key_price_limit)
            query['price_limit'] = price_limit
            key_filter['key_price_limit']=key_price_limit
        if key_machine_type:
            machine_type = Machine_type.objects.get(machine_type_name = key_machine_type)
            query['machine_type'] = machine_type
            key_filter['key_machine_type']=key_machine_type
        if key_wire_material:
            wire_material = Wire_material.objects.get(wire_material_name = key_wire_material)
            query['wire_material'] = wire_material
            key_filter['key_wire_material']=key_wire_material
        if key_categories:
            categories = Categories.objects.get(categories_name = key_categories)
            query['categories'] = categories
            key_filter['key_categories']=key_categories
        # if key_sex:
        #     query['sex'] = key_sex
        #     key_filter['key_trademark']=key_trademark

        list_clock = Clock.objects.filter(**query)
        context['list_clock'] = list_clock
        print('list_clock:',list_clock)
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material
        list_categories = Categories.objects.all()
        context['list_categories'] = list_categories
        

        return render(request, 'client/filter_page.html', context, status=200)   


def cart_page(request):
    if request.method == 'GET':
        cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
        cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python

        list_cart = []
        total = {"number":0,"money":0}
        if cart_items:
            for item_id in cart_items:
                try:
                    clock = Clock.objects.get(pk=int(item_id['id']))  # Lấy đối tượng Clock từ id
                    obj_item = {"obj": clock, "number": item_id['number'],}
                    list_cart.append(obj_item)
                    total['number'] = int(total['number']) + 1
                    if obj_item['number'] and obj_item['obj']:
                        total['money'] = int(total['money']) + int(obj_item['number'])*int(obj_item['obj'].price_has_decreased)
                        if total['money'] > 10000000:
                            total['money'] = int(total['money']) - (int(total['money']*10/100))

                except Clock.DoesNotExist:
                    pass  # Xử lý ngoại lệ nếu không tìm thấy đối tượng

        context = {'list_cart': list_cart,'total':total}
        if list_cart:
            list_voucher = Promotions.objects.all()
            list_voucher_filter = []
            list_clock = Clock.objects.filter(clock_name = clock)
            context['list_clock']=list_clock

            for i in list_voucher:
                a = is_voucher_valid(i.promotions_id)
                print('a:',a)
                if a:
                    list_voucher_filter.append(i)
            context['list_voucher_filter']=list_voucher_filter
        return render(request, 'client/cart_page.html', context)
    elif request.method == 'POST':
        number_product = request.POST.get('number_product')
        print('number_product:',number_product)
        if not number_product:
            number_product = 1
        id_add_cart = request.POST.get('id_add_cart')
        print('id_add_cart:',id_add_cart)
        item_id = {"id": id_add_cart, "number": number_product}

        cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
        cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python

        # Kiểm tra nếu mặt hàng đã có trong giỏ hàng
        item_exists = False
        for item in cart_items:
            if item["id"] == id_add_cart:
                item["number"] = int(item["number"]) + int(number_product) # Cộng thêm số lượng vào mặt hàng đã có
                item_exists = True
                break
        if not item_exists:
            # Nếu mặt hàng chưa tồn tại, thêm mặt hàng mới
            cart_items.append({"id": id_add_cart, "number": number_product})

        # Chuyển đổi lại cart_items thành JSON string và lưu vào cookie
        response = redirect('cart_page')  # Redirect về trang cart_page sau khi xử lý
        # response.set_cookie('cart', json.dumps(cart_items))  # Lưu cookie 'cart'
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)  # cookie sẽ hết hạn sau 7 ngày
        response.set_cookie(
            key='cart',
            value=json.dumps(cart_items),  # giá trị bạn muốn lưu trữ
            expires=expires
        )
        return response
def payment_online_page(request):
     if request.method == 'GET':
        context = {}
        list_order = Order.objects.filter(user_id=request.user.id)
        context['list_order'] = list_order
        return render(request, 'client/payment_online_page.html', context, status=200)

def delete_all_cart_page(request):
    if request.method == 'POST':
        cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
        cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python
        cart_items = []  # Xóa tất cả các mục trong giỏ hàng
        response = redirect('cart_page')  # Redirect về trang cart_page sau khi xử lý
        response.set_cookie('cart', json.dumps(cart_items))  # Lưu cookie 'cart'
        return response

def delete_cart_page(request):
    if request.method == 'POST':
        id_delete_cart = request.POST.get('id_delete_cart')
        print('id_delete_cart:',id_delete_cart)

        cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
        cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python

        cart_items = [item for item in cart_items if int(item['id']) != int(id_delete_cart)]
        # Chuyển đổi lại cart_items thành JSON string và lưu vào cookie
        response = redirect('cart_page')  # Redirect về trang cart_page sau khi xử lý
        response.set_cookie('cart', json.dumps(cart_items))  # Lưu cookie 'cart'
        return response
    
def update_number_cart_page(request):
    if request.method == 'POST':
        id_update_cart = request.POST.get('id_update_cart')
        print('id_update_cart:',id_update_cart)
        number_update_cart = request.POST.get('number_update_cart')
        print('number_update_cart:',number_update_cart)
        cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
        cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python
        for i in cart_items:
            if int(i['id'])==int(id_update_cart):
               
                i['number'] = int(number_update_cart)
        # Chuyển đổi lại cart_items thành JSON string và lưu vào cookie
        response = redirect('cart_page')  # Redirect về trang cart_page sau khi xử lý
        response.set_cookie('cart', json.dumps(cart_items))  # Lưu cookie 'cart'
        return response

def order_page(request):
    if request.method == 'GET':
        context = {}
        list_order = Order.objects.filter(user_id=request.user.id).select_related('promotion')
        context['list_order'] = list_order
        
    
        return render(request, 'client/order_page.html', context)
    if request.method == 'POST':
            def generate_random_code():
                return ''.join(random.choices(string.ascii_uppercase, k=8))
            
            code = generate_random_code()         
            name = request.POST.get('name')          
            phone = request.POST.get('phone')  
            address = request.POST.get('address')
            note = request.POST.get('note')
            code_voucher = request.POST.get('code_voucher')
        
        
            #lấy giỏ hàng từ cookie
            cart = request.COOKIES.get('cart', '[]')  # Lấy giá trị của cookie 'cart'
            cart_items = json.loads(cart)  # Chuyển đổi JSON string thành danh sách Python
            list_cart = []
            total = {"number":0,"money":0,"price":0}

            if not cart_items:
            # Nếu giỏ hàng trống, chuyển hướng người dùng về trang giỏ hàng hoặc hiển thị thông báo lỗi
                return redirect('cart_page')  # Hoặc render một thông báo lỗi

            if cart_items:
                for item_id in cart_items:
                    try:
                        clock = Clock.objects.get(pk=int(item_id['id']))  # Lấy đối tượng Clock từ id
                        obj_item = {"obj": clock, "number": item_id['number']}
                        list_cart.append(obj_item)
                        total['number'] = int(total['number']) + int(item_id['number'])
                        if obj_item['number'] and obj_item['obj']:
                            total['price']= int(obj_item['obj'].price_has_decreased)*int(obj_item['number'])
                            total['money'] = total['money'] + int(obj_item['number'])*int(obj_item['obj'].price_has_decreased)
                    except Clock.DoesNotExist:
                        pass  # Xử lý ngoại lệ nếu không tìm thấy đối tượng
            
            total_amount = total['number']
            total_pay = total['money']
            total_price_clock = total['price']
            context = {}
            obj_Promotions = None

            # Áp dụng mã giảm giá nếu có
            if code_voucher == 'Chọn mã giảm giá':
                code_voucher = None
                decrease_money = 0
                total_pay = int(total_pay) - decrease_money
                context['obj_Promotions'] = None
            else:
                try:
                    obj_Promotions = Promotions.objects.get(promotions_code = code_voucher)
                    promotions_discount_percent = obj_Promotions.promotions_discount_percent
                
                    decrease_money = (obj_Promotions.promotions_discount_percent/100)*total_pay
                    if decrease_money >  obj_Promotions.promotions_discount:
                        decrease_money = obj_Promotions.promotions_discount
                    total_pay = int(total_pay) - decrease_money 
                    payment_type = request.POST.get('payment_type')
                    obj_Promotions.amount = obj_Promotions.amount - 1
                    obj_Promotions.save()
                    context['obj_Promotions'] = obj_Promotions 
                except Promotions.DoesNotExist:
                    decrease_money = 0
                    context['obj_Promotions'] = None
            if int(total['number']) <= int(clock.quantity):
                 # Tạo đơn hàng mới
                obj_Order = Order.objects.create(
                                user_id = request.user,
                                code=code,
                                name=name,
                                phone=phone,
                                address=address,
                                note=note,
                                total_amount=total_amount,
                                total_pay=total_pay,
                                total_price=total_price_clock,
                                payment_type = payment_type,
                                promotion=obj_Promotions,
                            )
                clock.quantity = int(clock.quantity) - int(total['number'])
                clock.save()
            # Tạo chi tiết đơn hàng
                list_total_money=[]
                if obj_Order:
                    for i in list_cart:
                            try:
                                total_money=int(i['number']) * int(i['obj'].price_has_decreased) 
                                list_total_money.append({"obj": i['obj'], "total_money": total_money})
                                print('total_money:',total_money)
                                Orderdetails.objects.create(
                                order=obj_Order,
                                clock=i['obj'],
                                quantity=i['number'],
                                total_money=total_money
                            )
                            except Clock.DoesNotExist:
                                pass  # Xử lý ngoại lệ nếu không tìm thấy đối tượng

                    # Xóa giỏ hàng và chuyển hướng
                    response = redirect('order_page')  # Redirect về trang cart_page sau khi xử lý
                    # Xóa cookie 'cart'
                    response.delete_cookie('cart')
            else:
                messages.error(request, 'Số lượng trong kho không đủ để tạo thành đơn hàng')
                return redirect('cart_page')
            return response
            
def delete_order(request,pk):
    if request.method == 'GET':
        try:
            # Lấy đơn hàng để xóa
            order = Order.objects.get(pk=pk)
            
            # Lấy các chi tiết đơn hàng liên quan đến đồng hồ
            order_details = Orderdetails.objects.filter(order=order)
            
            # Cập nhật số lượng đồng hồ dựa trên chi tiết đơn hàng
            for detail in order_details:
                clock = detail.clock
                if clock.quantity:
                    # Cập nhật số lượng đồng hồ
                    clock.quantity = str(int(clock.quantity) + detail.quantity)
                    clock.save()
            
            # Xóa các chi tiết đơn hàng
            order_details.delete()
            
            # Xóa đơn hàng
            order.delete()
            
            # Redirect về trang đơn hàng
            return redirect('order_page')
        
        except Order.DoesNotExist:
            raise Http404("Order does not exist")

def detail_clock_page(request,pk):
    if request.method == 'GET':
        context = {}
        detail_clock = Clock.objects.get(pk=pk)
        context['detail_clock'] = detail_clock
        obj_clock = Clock.objects.get(clock_id=pk)
        list_comment = Comment.objects.filter(clock_id=obj_clock)
        context['list_comment']=list_comment
        return render(request, 'client/detail_clock_page.html', context, status=200)
    if request.method == 'POST':
        id_detail = request.POST.get('id_detail')
        content = request.POST.get('content')
        obj_clock = Clock.objects.get(clock_id=pk)
        Comment.objects.create(
                            user_name = request.user,
                            clock_id=obj_clock,
                            cmt = content
                        )
        return redirect('detail_clock_page',pk=id_detail)
        
# login,logout //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def user_logout(request):
    # User.objects.create_user(username='vy',password='vy',email='vy@gmail.com')
    logout(request)
    # Đăng xuất thành công, redirect đến trang đăng nhập hoặc trang khác tuỳ chọn
    return redirect('login')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username dn:',username)
        print('password dn:',password)
        user = authenticate(request, username=username, password=password)
        print('user tk:',user)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('page_admin')
            else:
                return redirect('profile')
        else:
            # Đăng nhập không thành công, hiển thị thông báo lỗi
            request.session['error_login'] = 'Tên người dùng hoặc mật khẩu không đúng !'
            messages.error(request, 'Tên người dùng hoặc mật khẩu không đúng.')
            context = {'name':'vy'}
            return redirect('login')
    if request.method == 'GET':
        context = {'name':'vy'}
        if 'error_login' in request.session:
            error = request.session.get('error_login')
            context ['error_login'] = error
            del request.session['error_login']
        if request.user.is_authenticated:
            return redirect('profile')
        return render(request, 'client/login.html', context, status=200)
    
def user_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            request.session['error_register'] = 'Email đã tồn tại'
        elif User.objects.filter(username=username).exists():
            request.session['error_register'] = "Tên tài khoản đã tồn tại"
        elif User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
            request.session['error_register'] = "Email và Tên tài khoản đã tồn tại"
        else:
            User.objects.create_user(email=email,username=username,password=password)
            request.session['register_created'] = True
        return redirect('register')
    if request.method == 'GET':
        context = {'name':'vy'}
        if 'register_created' in request.session:
            register_created = request.session.get('register_created')
            context ['register_created'] = register_created
            del request.session['register_created']
        if 'error_register' in request.session:
            error_register = request.session.get('error_register')
            context ['error_register'] = error_register
            del request.session['error_register']
        return render(request, 'client/register.html', context, status=200)
    
def user_profile(request):
    if request.method == 'GET':
        context = {'name':'vy'}
        if request.user.is_authenticated:
            return render(request, 'client/profile_page.html', context, status=200)
        else:
            return redirect('login')
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user  # Lấy thông tin người dùng đăng nhập

            # Lấy thông tin từ form
            user.user_name = request.POST.get('user_name')
            user.user_phone = request.POST.get('user_phone')
            user.user_address = request.POST.get('user_address')
            user.user_birthday = request.POST.get('user_birthday')

            # Kiểm tra nếu có nhập mật khẩu mới
            new_password = request.POST.get('password')
            if new_password:
                user.set_password(new_password)  # Cập nhật mật khẩu mới
                update_session_auth_hash(request, user)  # Cập nhật session để người dùng không bị đăng xuất
            # Kiểm tra nếu có nhập mật khẩu mới
            new_Cus_avatar = request.FILES.get('user_avatar')
            if new_Cus_avatar:
                user.user_avatar = new_Cus_avatar  # Cập nhật mật khẩu mới

            user.save()  # Lưu thông tin người dùng vào cơ sở dữ liệu
            return redirect('profile')
        
        
def user_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'client/register.html', context, status=200)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = create_user(username,password)
        context = {'obj': obj}
        return render(request, 'client/register.html', context, status=200)
    return HttpResponse("Method not allowed", status=405)  # Thêm phản hồi cho các phương thức khác
        