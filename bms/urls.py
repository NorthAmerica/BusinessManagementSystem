from django.urls import path
from . import views
from bms.ui_views import main_user_views,user_group_view

app_name = 'bms'

urlpatterns = [
	path('login',views.login_page,name='login'),
	path('logout',views.Logout_page,name='logout'),
	path('login_check',views.login_check,name='login_check'),
	path('index', views.index, name='index'),
	path('main_user_list',main_user_views.main_user_list, name='main_user_list'),
	path('add_main_user',main_user_views.add_main_user,name='add_main_user'),
	path('update_main_user',main_user_views.update_main_user,name='update_main_user'),
	path('change_pwd_main_user',main_user_views.change_pwd_main_user,name='change_pwd_main_user'),

	path('user_group',user_group_view.user_group,name='user_group'),
	path('group_list',user_group_view.group_list,name='group_list')
]
