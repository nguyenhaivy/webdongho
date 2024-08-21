from .models import *

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator


from django.http import HttpResponse
import requests
import time

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

def create_user(username,password,role):
    obj = User.objects.create_user(username=username,password=password,role=role)
    return obj
 
def create_user_admin(username,password,email,user_name,user_phone,user_address,user_birthday,user_avatar,role):
    obj = User.objects.create_user(username=username,
                                   password=password,
                                   email=email,
                                   user_name=user_name,
                                   user_phone=user_phone,
                                   user_address=user_address,
                                   user_birthday=user_birthday,
                                   user_avatar=user_avatar,
                                   role=role,
                                   )
    return obj

def get_user(pk):
    obj = User.objects.get(pk=pk)
    return obj

def update_user_admin(pk,password,email,user_name,user_phone,user_address,user_birthday,user_avatar):
    obj = User.objects.get(pk=pk)

    obj.email = email
    obj.user_name=user_name
    obj.user_phone=user_phone
    obj.user_address=user_address
    obj.user_birthday=user_birthday

    if user_avatar:
        obj.user_avatar=user_avatar

    if password:
        obj.set_password(password)  

    obj.save()
def create_voucher_admin(promotions_code,promotions_name,promotions_discount,promotions_discount_percent,amount,start_time,end_time):
    obj = Promotions.objects.create(promotions_code=promotions_code,
                                   promotions_name=promotions_name,
                                   promotions_discount=promotions_discount,
                                   promotions_discount_percent=promotions_discount_percent,
                                   amount=amount,
                                   start_time=start_time,
                                   end_time=end_time,
                                   )
    return obj
def create_post_admin(title,content,post_date,image):
    obj = Post.objects.create(title=title,
                                   content=content,
                                   post_date=post_date,
                                   image=image
                                   )
    return obj

def get_voucher(pk):
    try:
        obj = Promotions.objects.get(pk=pk)
        return obj
    except Promotions.DoesNotExist:
        return None
    
def is_voucher_valid(pk):
    promotion = get_voucher(pk)
    if not promotion:
        return False
    
    try:
        start_time = promotion.start_time
        end_time = promotion.end_time
    except AttributeError:
        # Xử lý trường hợp voucher không có các thuộc tính này
        return False
    
    current_time = timezone.now()
    return start_time <= current_time <= end_time

#Phần Client
