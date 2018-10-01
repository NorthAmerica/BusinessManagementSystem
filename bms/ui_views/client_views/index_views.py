from django.shortcuts import render, get_list_or_404
from bms.tool_kit.fund_shortcuts import get_client_balance

def index(request):
	client_balance = get_client_balance(request.session.get('client_id'))
	return render(request, 'bms/client_ui/weui-tab.html',locals())