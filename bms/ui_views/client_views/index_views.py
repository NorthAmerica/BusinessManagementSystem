from django.shortcuts import render, get_list_or_404
from bms.tool_kit.fund_shortcuts import get_client_balance
from bms.tool_kit.client_shortcuts import get_client_msg_num
from django.http import HttpResponseRedirect
from bms.tool_kit.views_decorator import Check_Login

@Check_Login('/login')
def index(request):
	client_balance = get_client_balance(request.session.get('client_id'))
	client_msg_num = get_client_msg_num(request.session.get('client_id'))
	return render(request, 'bms/client_ui/weui-tab.html',locals())

def redirect_pre_page(request,path):
	'''返回上页'''
	if request.method == 'GET' and path is not None:
		# path = request.GET.get('path')
		if str(path).endswith('/'):
			direct = str(path)[:str(path).__len__()-1]
			return HttpResponseRedirect(direct)
		else:
			return HttpResponseRedirect(path)