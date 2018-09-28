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
    path('login', login_views.login),
	path('register', login_views.register),
	path('login_check', login_views.login_check),
	path('reg_check', login_views.reg_check),
	path('logout',login_views.logout),
	path('my_account', my_views.my_account),
	path('authentication',my_views.authentication),
	path('update_authentication_info',my_views.update_authentication_info),
	path('checking',my_views.checking),

    path('bms/',include('bms.urls')),
    path('admin/', admin.site.urls),
]
