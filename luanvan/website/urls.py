"""
URL configuration for luanvan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from Data_Interaction.admin import admin_site
from django.urls import path

from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import re_path,path


from django.views.generic.base import TemplateView
from django.conf.urls.static import serve

from django.views.generic import RedirectView

from .controller_client import *
from .controller_admin import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', home,name='home'),
    path('home', home_page,name='home_page'),

    path('installment/<int:pk>/', installment_page,name='installment_page'),
    path('order-installment/<int:pk>/', order_installment_page,name='order_installment_page'),
    path('period/', period_installment_page,name='period_installment_page'),
    path('settled/', amount_settled_page,name='amount_settled_page'),
    path('payment-page/', payment_page,name='payment_page'),
    path('settled-payment-page/', Settled_payment_page,name='Settled_payment_page'),


    path('detail-post-page/<int:pk>/', detail_post_page,name='detail_post_page'),

    path('cart/', cart_page,name='cart_page'),
    
    path('payment-online/', payment_online_page,name='payment_online_page'),
    path('cart-delete/', delete_cart_page,name='delete_cart_page'),
    path('cart-update/', update_number_cart_page,name='update_number_cart_page'),
    path('detail-clock-page/<int:pk>/', detail_clock_page,name='detail_clock_page'),
    
    path('filter-clock/', filter_clock,name='filter_clock'),

    path('order/', order_page,name='order_page'),
    path('order-delete/<int:pk>/', delete_order,name='delete_order'),

    path('login/', user_login,name='login'),
    path('register/', user_register,name='register'),
    path('profile/', user_profile,name='profile'),
    path('logout/', user_logout,name='logout'),
    path('user/', user_page,name='user_page'),

    path('admin/dashboard/',dashboard,name='dashboard'),
    path('admin/chart-user/',chart_user,name='chart_user'),
    path('admin/chart-order/',chart_order,name='chart_order'),
    path('admin/chart-voucher/',chart_voucher,name='chart_voucher'),
    path('admin/chart-installment/',chart_installment,name='chart_installment'),
   
    path('admin/installment-order/', installment_order_page,name='installment_order_page'),
    path('admin/accept-installment-order/', accept_installment,name='accept_installment'),
    path('admin/installment/',admin_installment_page,name='admin_installment_page'),
    path('admin/installment-order-detail/<int:pk>/', installment_order_detail,name='installment_order_detail'),
     path('admin/delete-installment-page/<int:pk>/',delete_installment_page,name='delete_installment_page'),

    path('admin/voucher/', voucher_page,name='voucher_page'),
    path('add-voucher-page/',add_voucher_page,name='add_voucher_page'),
    path('delete-voucher-page/<int:pk>/',delete_voucher_page,name='delete_voucher_page'),


    path('admin/post/', post_page,name='post_page'),
    path('add-post-page/',add_post_page,name='add_post_page'),
   
   
    path('admin/', page_admin,name='page_admin'),
    path('add-clock-page/',add_clock_page,name='add_clock_page'),
    path('delete-clock-page/<int:pk>/',delete_clock_page,name='delete_clock_page'),
    path('update-user-page/<int:pk>/',update_user_page,name='update_user_page'),

    path('admin/user/', page_user,name='page_user'),
    path('add-user-page/',add_user_page,name='add_user_page'),
    path('delete-user-page/<int:pk>/',delete_user_page,name='delete_user_page'),
    path('update-clock-page/<int:pk>/',update_clock_page,name='update_clock_page'),



    path('admin/order/', page_order,name='page_order'),
    path('delete-order-page/<int:pk>/',delete_order_page,name='delete_order_page'),
    path('update-status-order/<str:st>/<int:pk>/',update_status_order_page,name='update_status_order_page'),
    

    path('add-categories-page/',add_categories_page,name='add_categories_page'),
    path('delete-categories-page/<int:pk>/',delete_categories_page,name='delete_categories_page'),
    path('update-categories-page/',update_categories_page,name='update_categories_page'),

    path('add-trademark-page/',add_trademark_page,name='add_trademark_page' ),
    path('delete-trademark-page/<int:pk>/',delete_trademark_page,name='delete_trademark_page'),
    path('update-trademark-page/',update_trademark_page,name='update_trademark_page'),


    path('add-price-limit-page/',add_price_limit_page,name='add_price_limit_page' ),
    path('delete-price-limit-page/<int:pk>/',delete_price_limit_page,name='delete_price_limit_page'),
    path('update-price-limit-page/',update_price_limit_page,name='update_price_limit_page'),

    path('add-machine-type-page/',add_machine_type_page,name='add_machine_type_page' ),
    path('delete-machine-type-page/<int:pk>/',delete_machine_type_page,name='delete_machine_type_page'),
    path('update-machine-type-page/',update_machine_type_page,name='update_machine_type_page'),

    path('add-wire-material-page/',add_wire_material_page,name='add_wire_material_page' ),
    path('delete-wire-material-page/<int:pk>/',delete_wire_material_page,name='delete_wire_material_page'),
    path('update-wire-material-page/',update_wire_material_page,name='update_wire_material_page'),
]