from django.conf.urls import url
from django.urls import path, include
from . import views
from bms.ui_views import main_user_views,user_group_view,agency_views,client_config_views,order_views,rule_views,msg_views

app_name = 'bms'

urlpatterns = [
	# 首页
	path('login',views.login_page,name='login'),
	path('logout',views.Logout_page,name='logout'),
	path('login_check',views.login_check,name='login_check'),
	path('index', views.index, name='index'),
	path('change_pwd_page',views.change_pwd_page,name='change_pwd_page'),
	path('change_pwd',views.change_pwd,name='change_pwd'),
	# 消息管理
	path('show_msg_num',msg_views.show_msg_num,name='show_msg_num'),
	path('msg_list',msg_views.msg_list,name='msg_list'),
	path('msg_detail',msg_views.msg_detail,name='msg_detail'),
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
	# 归属管理
	path('agency_config', agency_views.agency_config, name='agency_config'),
	path('agency_user_config',agency_views.agency_user_config,name='agency_user_config'),
	path('get_agency_group',agency_views.get_agency_group,name='get_agency_group'),
	path('agency_group_config',agency_views.agency_group_config,name='agency_group_config'),
	path('get_agency_tree', agency_views.get_agency_tree, name='get_agency_tree'),
	path('get_agency_list', agency_views.get_agency_list, name='get_agency_list'),
	path('add_agency',agency_views.add_agency,name='add_agency'),
	path('update_agency',agency_views.update_agency,name='update_agency'),
	path('get_allow_business',agency_views.get_allow_business,name='get_allow_business'),
	# 配置管理
	path('fund_in_config',rule_views.fund_in_config,name='fund_in_config'),
	path('get_org_tree',rule_views.get_org_tree,name='get_org_tree'),
	path('get_global_fund_in',rule_views.get_global_fund_in,name='get_global_fund_in'),
	path('add_fund_in',rule_views.add_fund_in,name='add_fund_in'),
	path('get_global_fund_out',rule_views.get_global_fund_out,name='get_global_fund_out'),
	path('add_fund_out',rule_views.add_fund_out,name='add_fund_out'),
	path('fund_out_config',rule_views.fund_out_config,name='fund_out_config'),
	path('exchange_config',rule_views.exchange_config,name='exchange_config'),
	path('get_exchange_rule',rule_views.get_exchange_rule,name='get_exchange_rule'),
	path('add_exchange_rule',rule_views.add_exchange_rule,name='add_exchange_rule'),
	path('notional_principal_config',rule_views.notional_principal_config,name='notional_principal_config'),
	path('get_notional_principal',rule_views.get_notional_principal,name='get_notional_principal'),
	# 客户管理
	path('client_list',client_config_views.client_list,name='client_list'),
	path('get_client_list',client_config_views.get_client_list,name='get_client_list'),
	# 订单管理
	path('order_list',order_views.order_list,name='order_list'),
]
