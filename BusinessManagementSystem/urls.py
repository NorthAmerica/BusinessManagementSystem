"""BusinessManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from bms.ui_views.client_views import index_views, my_views, login_views

urlpatterns = [
    path('index', index_views.index),
	path('redirect_pre_page<path:path>',index_views.redirect_pre_page),
    path('login', login_views.login),
	path('register', login_views.register),
	path('login_check', login_views.login_check),
	path('reg_check', login_views.reg_check),
	path('logout',login_views.logout),
	path('my_account', my_views.my_account),
	path('authentication',my_views.authentication),
	path('update_authentication_info',my_views.update_authentication_info),
	path('checking',my_views.checking),
	path('change_pwd_page',my_views.change_pwd_page),
	path('change_pwd',my_views.change_pwd),
	# 出入金
	path('recharge_page',my_views.recharge_page),
	path('recharge',my_views.recharge),
	path('withdraw_page',my_views.withdraw_page),
	path('withdraw',my_views.withdraw),

	path('statement',my_views.statement),
	path('msg_center',my_views.msg_center),
	path('msg_detail/<int:msg_id>',my_views.msg_detail),

    path('bms/',include('bms.urls')),
    path('admin/', admin.site.urls),
]
