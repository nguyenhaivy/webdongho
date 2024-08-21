from .models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
import requests
import time

from django.db import models
from django.utils import timezone
import os

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from django.shortcuts import render
from .models import Installment, Promotions
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from datetime import datetime, timedelta

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

from datetime import datetime
from dateutil.relativedelta import relativedelta

def page_admin(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            list_clock = Clock.objects.all()
            context['list_clock'] = list_clock
            paginator = Paginator(list_clock, 5)
            page_number = request.GET.get('page')
            try:
                clocks = paginator.page(page_number)
            except PageNotAnInteger:
                clocks = paginator.page(1)
            except EmptyPage:
                clocks = paginator.page(paginator.num_pages)
            context['clocks'] = clocks
            return render(request, 'admin/clock_page.html', context, status=200, )
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            list_clock = Clock.objects.all()
            context['list_clock'] = list_clock
            paginator = Paginator(list_clock, 5)
            page_number = request.GET.get('page')
            try:
                clocks = paginator.page(page_number)
            except PageNotAnInteger:
                clocks = paginator.page(1)
            except EmptyPage:
                clocks = paginator.page(paginator.num_pages)
            context['clocks'] = clocks
            return render(request, 'admin/clock_page.html', context, status=200)
        else:
            return redirect('login')

def installment_order_page(request):
     if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            list_installment = Installment.objects.all()
            context['list_installment'] = list_installment
            return render(request, 'admin/installment_order_page.html', context, status=200)
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            list_installment = Installment.objects.all()
            context['list_installment'] = list_installment
            return render(request, 'admin/installment_order_page.html', context, status=200)
        else:
            return redirect('login')
def installment_order_detail(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            obj = Installment.objects.get(pk=pk)
            list_period_pay =  Installment_Period.objects.filter(installment_id = obj,period=True)
            amount_of_payment_left = str(len(list_period_pay))+'/'+ str(obj.number_of_payments)
            context['amount_of_payment_left']=amount_of_payment_left
            print('amount_of_payment_left:',amount_of_payment_left)
            if str(len(list_period_pay)) ==  str(obj.number_of_payments):
                obj.status = "Hoàn Tất"
                obj.save()
            context['obj'] = obj
            return render(request, 'admin/installment_order_detail.html', context, status=200)
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            obj = Installment.objects.get(pk=pk)
            list_period_pay =  Installment_Period.objects.filter(installment_id = obj,period=True)
            amount_of_payment_left = str(len(list_period_pay))+'/'+ str(obj.number_of_payments)
            context['amount_of_payment_left']=amount_of_payment_left
            print('amount_of_payment_left:',amount_of_payment_left)
            if str(len(list_period_pay)) ==  str(obj.number_of_payments):
                obj.status = "Hoàn Tất"
                obj.save()
            context['obj'] = obj
            return render(request, 'admin/installment_order_detail.html', context, status=200)
        else:
            return redirect('login')

def delete_installment_page(request,pk):
    if request.method == 'GET':
        Installment.objects.get(pk=pk).delete()
        return redirect('installment_order_page')



def chart_user(request):
    # Lấy số lượng người dùng theo vai trò
    users_by_role = (
        User.objects
        .values('role')
        .annotate(count=Count('id'))
        .order_by('role')
    )
    
    roles = [user['role'] for user in users_by_role]
    counts = [user['count'] for user in users_by_role]

    # Tạo biểu đồ
    fig = go.Figure(data=[go.Pie(labels=roles, values=counts)])
    fig.update_layout(title='Số lượng người dùng theo vai trò')
    
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    return render(request, 'admin/chart_user.html', {'graph_html': graph_html})

def chart_order(request):
      # Xác định tháng của năm hiện tại
    now = datetime.now()
    start_date = now.replace(day=1, month=1)  # Bắt đầu từ tháng 1 của năm hiện tại
    end_date = now.replace(day=1, month=12)  # Kết thúc vào tháng 12 của năm hiện tại

    # Tạo danh sách tất cả các tháng
    months_range = [start_date + timedelta(days=30 * i) for i in range(12)]
    months_labels = [date.strftime('%B %Y') for date in months_range]
    # Lấy số lượng đơn hàng theo từng tháng
    orders_per_month = (
        Order.objects
        .annotate(month=TruncMonth('creation_time'))
        .values('month')
        .annotate(count=Count('order_id'))
        .order_by('month')
    )
    
    order_data = {date.strftime('%B %Y'): 0 for date in months_range}
    for order in orders_per_month:
        month_label = order['month'].strftime('%B %Y')
        order_data[month_label] = order['count']

    # Tạo dữ liệu cho biểu đồ
    counts = [order_data[label] for label in months_labels]

    # Tạo biểu đồ
    fig = go.Figure(data=[go.Bar(x=months_labels, y=counts)])
    fig.update_layout(title='Số lượng đơn hàng theo tháng', xaxis_title='Tháng', yaxis_title='Số lượng đơn hàng')
    
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    return render(request, 'admin/chart_order.html', {'graph_html': graph_html})

def chart_voucher(request):
    now = datetime.now()
    start_date = now.replace(day=1, month=1)  # Bắt đầu từ tháng 1 của năm hiện tại
    end_date = now.replace(day=1, month=12)  # Kết thúc vào tháng 12 của năm hiện tại

    # Tạo danh sách tất cả các tháng
    months_range = [start_date + timedelta(days=30 * i) for i in range(12)]
    months_labels = [date.strftime('%B %Y') for date in months_range]

    # Lấy số lượng phiếu giảm giá theo từng tháng
    promotions_per_month = (
        Promotions.objects
        .annotate(month=TruncMonth('creation_time'))
        .values('month')
        .annotate(count=Count('promotions_id'))
        .order_by('month')
    )
    
    # Tạo dictionary để ánh xạ tháng với số lượng phiếu giảm giá
    promotions_data = {date.strftime('%B %Y'): 0 for date in months_range}
    for promo in promotions_per_month:
        month_label = promo['month'].strftime('%B %Y')
        promotions_data[month_label] = promo['count']

    # Tạo dữ liệu cho biểu đồ
    counts = [promotions_data[label] for label in months_labels]

    # Tạo biểu đồ
    fig = go.Figure(data=[go.Bar(x=months_labels, y=counts)])
    fig.update_layout(title='Số lượng phiếu giảm giá theo tháng', xaxis_title='Tháng', yaxis_title='Số lượng phiếu giảm giá')
    
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    return render(request, 'admin/chart_voucher.html', {'graph_html': graph_html})

def chart_installment(request):
    # Xác định tháng của năm hiện tại
    now = datetime.now()
    start_date = now.replace(day=1, month=1)  # Bắt đầu từ tháng 1 của năm hiện tại
    end_date = now.replace(day=1, month=12)  # Kết thúc vào tháng 12 của năm hiện tại

    # Tạo danh sách tất cả các tháng
    months_range = [start_date + timedelta(days=30 * i) for i in range(12)]
    months_labels = [date.strftime('%B %Y') for date in months_range]

    # Lấy số lượng đơn trả góp theo từng tháng
    installments_per_month = (
        Installment.objects
        .annotate(month=TruncMonth('creation_time'))
        .values('month')
        .annotate(count=Count('installment_id'))
        .order_by('month')
    )
    
    # Lấy số tiền tất toán theo từng tháng
    amount_settled_per_month = (
        Installment.objects
        .annotate(month=TruncMonth('creation_time'))
        .values('month')
        .annotate(total_settled=Sum('amount_settled'))
        .order_by('month')
    )
    
    # Lấy phân phối tình trạng đơn trả góp
    status_distribution = (
        Installment.objects
        .values('status')
        .annotate(count=Count('installment_id'))
    )

    # Tạo dữ liệu cho biểu đồ
    installments_data = {date.strftime('%B %Y'): 0 for date in months_range}
    amount_settled_data = {date.strftime('%B %Y'): 0 for date in months_range}
    status_data = {}

    for installment in installments_per_month:
        month_label = installment['month'].strftime('%B %Y')
        installments_data[month_label] = installment['count']

    for amount in amount_settled_per_month:
        month_label = amount['month'].strftime('%B %Y')
        amount_settled_data[month_label] = amount['total_settled'] or 0

    for status in status_distribution:
        status_data[status['status']] = status['count']

    # Tạo biểu đồ
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Số lượng đơn trả góp theo tháng',
            'Phân phối tình trạng đơn trả góp',
            'Số tiền tất toán theo tháng'
        ),
        specs=[[{'type': 'bar'}, {'type': 'pie'}],
               [{'type': 'bar'}, {'type': 'xy'}]]
    )

    # Biểu đồ số lượng đơn trả góp theo tháng
    fig.add_trace(
        go.Bar(x=months_labels, y=[installments_data[label] for label in months_labels]),
        row=1, col=1
    )

    # Biểu đồ phân phối tình trạng đơn trả góp
    fig.add_trace(
        go.Pie(labels=list(status_data.keys()), values=list(status_data.values())),
        row=1, col=2
    )

    # Biểu đồ số tiền tất toán theo tháng
    fig.add_trace(
        go.Bar(x=months_labels, y=[amount_settled_data[label] for label in months_labels]),
        row=2, col=1
    )

    fig.update_layout(title='Biểu đồ tổng hợp', height=800, width=1000)
    
    graph_html = plot(fig, include_plotlyjs=True, output_type='div')
    return render(request, 'admin/chart_installment.html', {'graph_html': graph_html})


def dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            count_user_admin = 0
            count_user = 0
            count_order_status_cxn = 0
            count_order_status_dxn = 0
            count_order_status_dgh = 0
            count_order_status_dagh = 0
            count_voucher_is_valid = 0
            count_voucher_expired = 0
            count_installment_dc = 0
            count_installment_ht = 0
            count_installment_dn = 0

            list_order = Order.objects.all()
            for i in list_order:
                if i.status == 'Chờ Xác nhận':
                    count_order_status_cxn += 1
                elif i.status == 'Đã xác nhận':
                    count_order_status_dxn += 1
                elif i.status == 'Đang giao hàng':
                    count_order_status_dgh += 1
                elif i.status == 'Đã giao hàng':
                    count_order_status_dagh += 1
            context['count_order_status_cxn']=count_order_status_cxn
            context['count_order_status_dxn']=count_order_status_dxn
            context['count_order_status_dgh']=count_order_status_dgh
            context['count_order_status_dagh']=count_order_status_dagh
            print('count_order_status_cxn:',count_order_status_cxn)
            list_user = User.objects.all()
            for i in list_user:
                if i.role == 'User':
                    count_user += 1
                else:
                    count_user_admin += 1
            context['count_user_admin']=count_user_admin
            context['count_user']=count_user
            list_voucher = Promotions.objects.all()
            for i in list_voucher:
                    if is_voucher_valid(i.promotions_id):
                        count_voucher_is_valid += 1
                    else:
                        count_voucher_expired += 1
            context['count_voucher_is_valid'] = count_voucher_is_valid
            context['count_voucher_expired'] = count_voucher_expired
            list_installment = Installment.objects.all()
            for i in list_installment:
                if i.status == 'Đang Chạy':
                    count_installment_dc +=1
                elif i.status == 'Hoàn Tất':
                    count_installment_ht +=1
                else:
                    count_installment_dn +=1
            context['count_installment_dc'] = count_installment_dc
            context['count_installment_ht'] = count_installment_ht
            context['count_installment_dn'] = count_installment_dn
            context['len_list_order'] = len(list_order)
            context['len_list_user'] = len(list_user)
            context['len_list_voucher'] = len(list_voucher)
            context['len_list_installment'] = len(list_installment)
            

        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            count_user_admin = 0
            count_user = 0
            count_order_status_cxn = 0
            count_order_status_dxn = 0
            count_order_status_dgh = 0
            count_order_status_dagh = 0
            count_voucher_is_valid = 0
            count_voucher_expired = 0
            count_installment_dc = 0
            count_installment_ht = 0
            count_installment_dn = 0

            list_order = Order.objects.all()
            for i in list_order:
                if i.status == 'Chờ Xác nhận':
                    count_order_status_cxn += 1
                elif i.status == 'Đã xác nhận':
                    count_order_status_dxn += 1
                elif i.status == 'Đang giao hàng':
                    count_order_status_dgh += 1
                elif i.status == 'Đã giao hàng':
                    count_order_status_dagh += 1
            context['count_order_status_cxn']=count_order_status_cxn
            context['count_order_status_dxn']=count_order_status_dxn
            context['count_order_status_dgh']=count_order_status_dgh
            context['count_order_status_dagh']=count_order_status_dagh
            print('count_order_status_cxn:',count_order_status_cxn)
            list_user = User.objects.all()
            for i in list_user:
                if i.role == 'User':
                    count_user += 1
                else:
                    count_user_admin += 1
            context['count_user_admin']=count_user_admin
            context['count_user']=count_user
            list_voucher = Promotions.objects.all()
            for i in list_voucher:
                        if is_voucher_valid(i.promotions_id):
                            count_voucher_is_valid += 1
                        else:
                            count_voucher_expired += 1
            context['count_voucher_is_valid'] = count_voucher_is_valid
            context['count_voucher_expired'] = count_voucher_expired
            list_installment = Installment.objects.all()
            for i in list_installment:
                if i.status == 'Đang Chạy':
                    count_installment_dc +=1
                elif i.status == 'Hoàn Tất':
                    count_installment_ht +=1
                else:
                    count_installment_dn +=1
            context['count_installment_dc'] = count_installment_dc
            context['count_installment_ht'] = count_installment_ht
            context['count_installment_dn'] = count_installment_dn
            context['len_list_order'] = len(list_order)
            context['len_list_user'] = len(list_user)
            context['len_list_voucher'] = len(list_voucher)
            context['len_list_installment'] = len(list_installment)

        return render(request, 'admin/dashboard.html', context, status=200)

def generate_random_uppercase_code(length=8):
    # Tạo một chuỗi ngẫu nhiên gồm các chữ cái in hoa với độ dài xác định
    random_code = ''.join(random.choices(string.ascii_uppercase, k=length))
    return random_code

def accept_installment(request):
    if request.method=='POST':
        accept = request.POST.get('duyet')
        deny = request.POST.get('khongduyet')
        id = request.POST.get('id')
        obj= Installment.objects.get(pk=int(id))
        if accept:
            obj.status="Đang Chạy"
            obj.accept_time = datetime.now()
            obj.save()
            for i in range(int(obj.number_of_payments)):
                Installment_Period.objects.create(
                                                period_code = generate_random_uppercase_code(),
                                                period_name=i+1,
                                                period_amount=obj.amount_of_payment,
                                                period_day =  obj.accept_time + relativedelta(months=i+1),
                                                installment_id=obj
                                                )
        if deny:
            obj.status="Từ Chối"
        obj.save()
        return redirect('installment_order_page')

def admin_installment_page(request):
      if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            list_installment = Installment.objects.all()
            context['list_installment'] = list_installment
            return render(request, 'admin/installment_page.html', context, status=200)
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            list_installment = Installment.objects.all()
            context['list_installment'] = list_installment
            return render(request, 'admin/installment_page.html', context, status=200)
        else:
            return redirect('login')

def add_clock_page(request):
    if request.method == 'GET':
        context = {}
        list_category = Categories.objects.all()
        context['list_category'] = list_category
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material

        # Check if there is an error message in session
        if 'error_clock_name' in request.session:
            context['error_clock_name'] = request.session.get('error_clock_name')
            del request.session['error_clock_name']  # Clear the error message after using it

        return render(request, 'admin/add_clock_page.html', context, status=200)
    
    if request.method == 'POST':
        clock_name = request.POST.get('clock_name')
        describe = request.POST.get('describe')

        categories_id = int(request.POST.get('categories'))
        trademark_id = int(request.POST.get('trademark'))
        price_limit_id = int(request.POST.get('price_limit'))
        machine_type_id = int(request.POST.get('machine_type'))
        wire_material_id = int(request.POST.get('wire_material'))

        try:
            categories = Categories.objects.get(categories_id=categories_id)
            trademark = Trademark.objects.get(trademark_id=trademark_id)
            price_limit = Price_limit.objects.get(price_id=price_limit_id)
            machine_type = Machine_type.objects.get(machine_type_id=machine_type_id)
            wire_material = Wire_material.objects.get(wire_material_id=wire_material_id)
        except Categories.DoesNotExist or Trademark.DoesNotExist or Price_limit.DoesNotExist or Machine_type.DoesNotExist or Wire_material.DoesNotExist:
            request.session['error_clock_name'] = 'Dữ liệu không hợp lệ'
            return redirect('add_clock_page')

        price = request.POST.get('price')
        sex = request.POST.get('sex')
        designs = request.POST.get('designs')
        glass_surface = request.POST.get('glass_surface')
        diameter = request.POST.get('diameter')
        face_color = request.POST.get('face_color')
        shell_material = request.POST.get('shell_material')
        water_resistance = request.POST.get('water_resistance')
        other_function = request.POST.get('other_function')
        brand_origin = request.POST.get('brand_origin')
        warranty_genuine = request.POST.get('warranty_genuine')
        percent_discount = request.POST.get('percent_discount')

        price_has_decreased = int(price) - (int(price) * (int(percent_discount) / 100))

        url = request.POST.get('url')
        quantity = request.POST.get('quantity')

        list_image = request.FILES.getlist('list_image')
        list_video = request.FILES.getlist('list_video')

        if Clock.objects.filter(clock_name=clock_name).exists():
            request.session['error_clock_name'] = 'Tên sản phẩm đã tồn tại'
            return redirect('add_clock_page')

        # Create the new clock entry
        obj = Clock.objects.create(
            clock_name=clock_name,
            describe=describe,
            categories=categories,
            trademark=trademark,
            price_limit=price_limit,
            machine_type=machine_type,
            wire_material=wire_material,
            price=price,
            sex=sex,
            designs=designs,
            glass_surface=glass_surface,
            diameter=diameter,
            face_color=face_color,
            shell_material=shell_material,
            water_resistance=water_resistance,
            other_function=other_function,
            brand_origin=brand_origin,
            warranty_genuine=warranty_genuine,
            percent_discount=percent_discount,
            price_has_decreased=price_has_decreased,
            url=url,
            quantity=quantity
        )
        
        for i in list_image:
            MediaImage.objects.create(image=i, belong_clock=obj)
        for i in list_video:
            MediaVideo.objects.create(video=i, belong_clock=obj)

        return redirect('page_admin')
def update_clock_page(request,pk):
    if request.method == 'GET':
        context = {}
        obj = Clock.objects.get(pk=pk)
        context['obj']=obj
        list_category = Categories.objects.all()
        context['list_category']=list_category
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type']=list_machine_type
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit']=list_price_limit
        list_trademark = Trademark.objects.all()
        context['list_trademark']=list_trademark
        list_wire_material=Wire_material.objects.all()
        context['list_wire_material']=list_wire_material
        return render(request, 'admin/update_clock_page.html', context, status=200)
    if request.method == 'POST':
        obj = Clock.objects.get(pk=pk)
        clock_name = request.POST.get('clock_name')
        describe = request.POST.get('describe')

        categories = request.POST.get('categories')
        categories = Categories.objects.get(categories_id=int(categories))

        trademark = request.POST.get('trademark')
        trademark = Trademark.objects.get(trademark_id=int(trademark))

        price_limit = request.POST.get('price_limit')
        price_limit = Price_limit.objects.get(price_id=int(price_limit))

        machine_type = request.POST.get('machine_type')
        machine_type = Machine_type.objects.get(machine_type_id=int(machine_type))

        wire_material = request.POST.get('wire_material')
        wire_material = Wire_material.objects.get(wire_material_id=int(wire_material))

        price = request.POST.get('price')
        sex = request.POST.get('sex')
        designs = request.POST.get('designs')
        glass_surface = request.POST.get('glass_surface')
        diameter = request.POST.get('diameter')
        face_color = request.POST.get('face_color')
        shell_material = request.POST.get('shell_material')
        water_resistance = request.POST.get('water_resistance')
        other_function = request.POST.get('other_function')
        brand_origin = request.POST.get('brand_origin')
        warranty_genuine = request.POST.get('warranty_genuine')
        percent_discount = request.POST.get('percent_discount')

        price_has_decreased = int(price)-(int(price)*(int(percent_discount)/100))

        url = request.POST.get('url')
        quantity = request.POST.get('quantity')

        list_image = request.FILES.getlist('list_image')
        list_video = request.FILES.getlist('list_video')

        obj.clock_name=clock_name
        obj.describe=describe
        obj.categories=categories
        obj.trademark=trademark
        obj.price_limit=price_limit
        obj.machine_type=machine_type
        obj.wire_material=wire_material
        obj.price=price
        obj.sex=sex
        obj.designs=designs
        obj.glass_surface=glass_surface
        obj.diameter=diameter
        obj.face_color=face_color
        obj.shell_material=shell_material
        obj.water_resistance=water_resistance
        obj.other_function=other_function
        obj.brand_origin=brand_origin
        obj.warranty_genuine=warranty_genuine
        obj.percent_discount=percent_discount
        obj.price_has_decreased=price_has_decreased
        obj.url=url
        obj.quantity=quantity
        obj.save()
        
        if list_image:
            list_image_old = obj.list_image_clock.all()
            list_image_old.delete()
            for i in list_image:
                MediaImage.objects.create(image=i,belong_clock=obj)
        if list_video:
            list_video_old = obj.list_video_clock.all()
            list_video_old.delete()
            for i in list_video:
                MediaVideo.objects.create(video=i,belong_clock=obj)

        return redirect('page_admin')

def delete_clock_page(request,pk):
    if request.method == 'GET':
        Clock.objects.get(pk=pk).delete()
        return redirect('page_admin')

def page_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            list_user = User.objects.all()
            context['list_user'] = list_user
            return render(request, 'admin/user_page.html', context, status=200)
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            list_user = User.objects.all()
            context['list_user'] = list_user
            return render(request, 'admin/user_page.html', context, status=200)
        else:
            return redirect('login')

def add_user_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'admin/add_user_page.html', context, status=200)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_name = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')
        user_address = request.POST.get('user_address')
        user_birthday = request.POST.get('user_birthday')
        user_avatar = request.FILES.get('user_avatar')
        role = request.POST.get('role')
        create_user_admin(username,password,email,user_name,user_phone,user_address,user_birthday,user_avatar,role)
        return redirect('page_user')

def update_user_page(request,pk):
    if request.method == 'GET':
        context = {}
        obj = get_user(pk)
        context['obj'] = obj
        return render(request, 'admin/update_user_page.html', context, status=200)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_name = request.POST.get('user_name')
        user_phone = request.POST.get('user_phone')
        user_address = request.POST.get('user_address')
        user_birthday = request.POST.get('user_birthday')
        user_avatar = request.FILES.get('user_avatar')

        update_user_admin(pk,password,email,user_name,user_phone,user_address,user_birthday,user_avatar)

        return redirect('page_user')
def delete_user_page(request,pk):
    if request.method == 'GET':
        User.objects.get(pk=pk).delete()
        return redirect('page_user')




def voucher_page(request):
   if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.role == "Admin":
                list_voucher_is_valid = []
                list_voucher = Promotions.objects.all()
                for i in list_voucher:
                    if is_voucher_valid(i.promotions_id):
                        list_voucher_is_valid.append(i)
                
                context = {
                    'list_voucher': list_voucher,
                    'list_voucher_is_valid': list_voucher_is_valid,
                }
                print('list_voucher_is_valid:', list_voucher_is_valid)
                return render(request, 'admin/voucher_page.html', context, status=200)
            else:
                return redirect('login')
        else:
            return redirect('login')
        
def add_voucher_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'admin/add_voucher_page.html', context, status=200)
    if request.method == 'POST':
        promotions_code = request.POST.get('promotions_code')
        promotions_name = request.POST.get('promotions_name')
        promotions_discount = request.POST.get('promotions_discount')
        promotions_discount_percent = request.POST.get('promotions_discount_percent')
        amount = request.POST.get('amount')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        create_voucher_admin(promotions_code,promotions_name,promotions_discount,promotions_discount_percent,amount,start_time,end_time)
        return redirect('voucher_page')

def delete_voucher_page(request,pk):
    if request.method == 'GET':
        Promotions.objects.get(pk=pk).delete()
        return redirect('voucher_page')



def post_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff :
            context = {}
            list_post = Post.objects.all()
            context['list_post'] = list_post
            return render(request, 'admin/post_page.html', context, status=200)
        elif request.user.is_authenticated and request.user.role == "Admin":
            context = {}
            list_post = Post.objects.all()
            context['list_post'] = list_post
            return render(request, 'admin/post_page.html', context, status=200)
        else:
            return redirect('login')

def add_post_page(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'admin/add_post_page.html', context, status=200)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_date = request.POST.get('post_date')
        image = request.FILES.get('image')
        
        create_post_admin(title,content,post_date,image)
        return redirect('post_page')

def page_order(request):
     if request.method == 'GET':
        if request.user.is_authenticated and (request.user.is_staff or request.user.role == "Admin"):
            context = {}
            list_order = Order.objects.all()
            paginator = Paginator(list_order, 5)
            context['list_order'] = list_order
            paginator = Paginator(list_order, 5)
            page_number = request.GET.get('page')
            try:
                orders = paginator.page(page_number)
            except PageNotAnInteger:
                orders = paginator.page(1)
            except EmptyPage:
                orders = paginator.page(paginator.num_pages)
            context['orders'] = orders
            return render(request, 'admin/order_page.html', context, status=200)
        else:
            return redirect('login')
        
def delete_order_page(request,pk):
    if request.method == 'GET':
        Order.objects.get(pk=pk).delete()
        return redirect('page_order')
    
def update_status_order_page(request, st, pk):
    if request.method == 'GET':
        # Lấy đối tượng đơn hàng hoặc trả về lỗi 404 nếu không tìm thấy
        obj = get_object_or_404(Order, pk=pk)
        
        # Ánh xạ mã trạng thái với trạng thái thực tế
        status_mapping = {
            's1': 'Chờ Xác nhận',
            's2': 'Đã xác nhận',
            's3': 'Đang giao hàng',
            's4': 'Đã giao hàng'
        }
        # Cập nhật trạng thái nếu mã trạng thái hợp lệ
        if st in status_mapping:
            obj.status = status_mapping[st]
            obj.save()
        else:
            # Xử lý mã trạng thái không hợp lệ (tuỳ chọn)
            print(f'Mã trạng thái không hợp lệ: {st}')
        
        # Chuyển hướng về trang danh sách đơn hàng
        return redirect('page_order')
#Phần danh mục
def add_categories_page(request):
    if request.method == 'GET':
        context = {}
        list_category = Categories.objects.all()
        context['list_category'] = list_category
        print('context:',context)
        return render(request, 'admin/add_categories_page.html', context, status=200)
    if request.method =="POST":
        categories_name = request.POST.get('categories_name')
        url = request.POST.get('url')
        Categories.objects.create(categories_name=categories_name,url=url)
        return redirect('add_categories_page')
def delete_categories_page(request,pk):
    if request.method == 'GET':
        Categories.objects.get(pk=pk).delete()
        context = {}
        list_category = Categories.objects.all()
        context['list_category'] = list_category
        print('context:',context)
        return redirect('add_categories_page')
def update_categories_page(request):
    if request.method =="POST":
        id = request.POST.get('id_update')
        print('id:',id)
        categories_name = request.POST.get('categories_name_update')
        url = request.POST.get('url_update')
        obj = Categories.objects.get(pk=id)
        obj.categories_name = categories_name
        obj.url = url
        obj.save()
        return redirect('add_categories_page')
# Phần thương hiệu
def add_trademark_page(request):
    if request.method == 'GET':
        context = {}
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        print('context:',context)
        return render(request, 'admin/add_trademark_page.html', context, status=200)
    if request.method =="POST":
        trademark_name = request.POST.get('trademark_name')
        url = request.POST.get('url')
        avatar = request.FILES.get('avatar')
        Trademark.objects.create(trademark_name=trademark_name,url=url,avatar=avatar)
        return redirect('add_trademark_page')
def delete_trademark_page(request,pk):
    if request.method == 'GET':
        Trademark.objects.get(pk=pk).delete()
        context = {}
        list_trademark = Trademark.objects.all()
        context['list_trademark'] = list_trademark
        print('context:',context)
        return redirect('add_trademark_page')
def update_trademark_page(request):
    if request.method =="POST":
        id = request.POST.get('id_update')
        print('id:',id)
        trademark_name = request.POST.get('trademark_name_update')
        url = request.POST.get('url_update')
        avatar_update = request.FILES.get('avatar_update')
        obj = Trademark.objects.get(pk=id)
        obj.trademark_name = trademark_name
        obj.url = url
        if avatar_update:
            obj.avatar = avatar_update
        obj.save()
        return redirect('add_trademark_page')
#Phần mức giá
def add_price_limit_page(request):
    if request.method == 'GET':
        context = {}
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        print('context:',context)
        return render(request, 'admin/add_pricelimit_page.html', context, status=200)
    if request.method =="POST":
        price_limit_name = request.POST.get('price_limit_name')
        url = request.POST.get('url')
        Price_limit.objects.create(price_limit_name=price_limit_name,url=url)
        return redirect('add_price_limit_page')
def delete_price_limit_page(request,pk):
    if request.method == 'GET':
        Price_limit.objects.get(pk=pk).delete()
        context = {}
        list_price_limit = Price_limit.objects.all()
        context['list_price_limit'] = list_price_limit
        print('context:',context)
        return redirect('add_price_limit_page')
def update_price_limit_page(request):
    if request.method =="POST":
        id = request.POST.get('id_update')
        print('id:',id)
        price_limit_name = request.POST.get('price_limit_name_update')
        url = request.POST.get('url_update')
        obj = Price_limit.objects.get(pk=id)
        obj.price_limit_name = price_limit_name
        obj.url = url
        obj.save()
        return redirect('add_price_limit_page')
#Phần loại máy
def add_machine_type_page(request):
     if request.method == 'GET':
        context = {}
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        print('context:',context)
        return render(request, 'admin/add_machinetype_page.html', context, status=200)
     if request.method =="POST":
        machine_type_name = request.POST.get('machine_type_name')
        url = request.POST.get('url')
        Machine_type.objects.create(machine_type_name=machine_type_name,url=url)
        return redirect('add_machine_type_page')
def delete_machine_type_page(request,pk):
    if request.method == 'GET':
        print(f'pk: {pk}')
        Machine_type.objects.get(pk=pk).delete()
        context = {}
        list_machine_type = Machine_type.objects.all()
        context['list_machine_type'] = list_machine_type
        print('context:',context)
        return redirect('add_machine_type_page')
def update_machine_type_page(request):
    if request.method =="POST":
        id = request.POST.get('id_update')
        print('id:',id)
        machine_type_name = request.POST.get('machine_type_name_update')
        url = request.POST.get('url_update')
        obj = Machine_type.objects.get(pk=id)
        obj.machine_type_name = machine_type_name
        obj.url = url
        obj.save()
        return redirect('add_machine_type_page')
#Phần chất liệu dây
def add_wire_material_page(request):
    if request.method == 'GET':
        context = {}
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material
        print('context:',context)
        return render(request, 'admin/add_wirematerial_page.html', context, status=200)
    if request.method =="POST":
        wire_material_name = request.POST.get('wire_material_name')
        url = request.POST.get('url')
        Wire_material.objects.create(wire_material_name=wire_material_name,url=url)
        return redirect('add_wire_material_page')
def delete_wire_material_page(request,pk):
    if request.method == 'GET':
        Wire_material.objects.get(pk=pk).delete()
        context = {}
        list_wire_material = Wire_material.objects.all()
        context['list_wire_material'] = list_wire_material
        print('context:',context)
        return redirect('add_wire_material_page')
def update_wire_material_page(request):
    if request.method =="POST":
        id = request.POST.get('id_update')
        print('id:',id)
        wire_material_name = request.POST.get('wire_material_name_update')
        url = request.POST.get('url_update')
        obj = Wire_material.objects.get(pk=id)
        obj.wire_material_name = wire_material_name
        obj.url = url
        obj.save()
        return redirect('add_wire_material_page')


