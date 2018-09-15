from django.urls import path
from . import views
from bms.ui_views import main_user_views,user_group_view,agency_views,client_views,order_views

app_name = 'bms'

urlpatterns = [
	path('login',views.login_page,name='login'),
	path('logout',views.Logout_page,name='logout'),
	path('login_check',views.login_check,name='login_check'),
	path('index', views.index, name='index'),
	# 管理员后台管理
	path('main_user_list',main_user_views.main_user_list, name='main_user_list'),
	path('add_main_user',main_user_views.add_main_user,name='add_main_user'),
	path('update_main_user',main_user_views.update_main_user,name='update_main_user'),
	path('change_pwd_main_user',main_user_views.change_pwd_main_user,name='change_pwd_main_user'),
	# 管理员组后台管理
	path('user_group',user_group_view.user_group,name='user_group'),
	path('group_list',user_group_view.group_list,name='group_list'),
	path('add_user_to_group',user_group_view.add_user_to_group,name='add_user_to_group'),
	path('remove_user_from_group',user_group_view.remove_user_from_group,name='remove_user_from_group'),
	# 代理管理
	path('agency_config', agency_views.agency_config, name='agency_config'),
	path('get_agency_tree', agency_views.get_agency_tree, name='get_agency_tree'),
	path('get_agency_list', agency_views.get_agency_list, name='get_agency_list'),
	# 客户管理
	path('client_list',client_views.client_list,name='client_list'),

	# 订单管理
	path('order_list',order_views.order_list,name='order_list'),
]
