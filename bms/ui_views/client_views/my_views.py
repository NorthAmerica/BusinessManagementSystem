from  decimal import Decimal
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponseNotFound
from django.contrib.auth.hashers import make_password,check_password
from bms.tool_kit.views_decorator import check_fund_rule,Check_Login
from BusinessManagementSystem import settings
from bms.models import *
from bms.tool_kit.view_shortcuts import date_joined_sort
from bms.tool_kit.fund_shortcuts import offline_client_balance
import os

@Check_Login('/login')
def my_account(request):

	try:
		account_list = []
		client_id = request.session.get('client_id', None)
		if client_id is not None:
			find_fund_detail = Fund_Detail.objects.filter(client__id=client_id).filter(
								fund_audit='agree').order_by('-date_joined')
			if find_fund_detail.exists():
				for fund_detail in find_fund_detail:
					fund_dict = {
						'balance_change': fund_detail.balance_change,
						'fund_audit':fund_detail.get_fund_audit_display(),
						'fund_state':fund_detail.get_fund_state_display(),
						'fund_type':fund_detail.get_fund_type_display(),
						'balance_after':fund_detail.balance_after,
						'balance_before':fund_detail.balance_before,
						'date_joined':fund_detail.date_joined,
						'serial_number':fund_detail.serial_number
					}
					account_list.append(fund_dict)
		return render(request,'bms/client_ui/account/my_account.html',locals())
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)


@Check_Login('/login')
def authentication(request):
	return render(request,'bms/client_ui/account/authentication.html')

@Check_Login('/login')
def update_authentication_info(request):
	'''上传实名认证信息'''
	try:
		if request.method=='POST':
			bank_card = request.FILES.get('bank_card')
			mobile_phone = request.session.get('mobile_phone', None) if request.session.get('mobile_phone', None) is not None else '000'
			db_url = "bank/{id}/{file}".format(id=mobile_phone, file=bank_card._name)
			save_url = "bank/{id}/".format(id=mobile_phone)
			url = os.path.join(settings.MEDIA_ROOT, save_url)
			if not os.path.exists(url):
				os.makedirs(url)
			dest = os.path.join(settings.MEDIA_ROOT,save_url,bank_card._name)
			if os.path.exists(dest):
				os.remove(dest)
			with open(dest, "wb+") as destination:
				for chunk in bank_card.chunks():
					destination.write(chunk)

			card_no = request.POST.get('card_no',None)
			id_no = request.POST.get('id_no',None)
			bank_name = request.POST.get('bank_name',None)
			bank_city = request.POST.get('bank_city',None)
			branch_name = request.POST.get('branch_name',None)

			dic = {
				'identity_card':id_no,
				'bank_image':db_url,
				'bank_card':card_no,
				'bank_name':bank_name,
				'open_city':bank_city,
				'bank_branch':branch_name,
				'status':2
			}
			update_count = Client.objects.filter(pk=request.session.get('client_id')).update(**dic)
			if update_count!=0:
				request.session['status']='2'
				return JsonResponse({'success': True, 'msg': '认证信息上传成功！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

@Check_Login('/login')
def checking(request):
	'''等待审核通过页面'''
	return render(request,'bms/client_ui/account/checking.html')

@Check_Login('/login')
def change_pwd_page(request):
	'''修改密码页面'''
	return render(request,'bms/client_ui/account/change_pwd.html')

@Check_Login('/login')
def change_pwd(request):
	'''修改密码'''
	try:
		if request.method=='POST':
			old_pwd = request.POST.get('old_pwd')
			new_pwd = request.POST.get('new_pwd')

			find_client = Client.objects.filter(pk=request.session.get('client_id'))
			if find_client.exists():
				client = find_client.first()
				if check_password(old_pwd,client.password):
					dic = {
						'password': make_password(new_pwd)
					}
					update_count = Client.objects.filter(pk=request.session.get('client_id')).update(**dic)
					if update_count != 0:
						return JsonResponse({'success': True, 'msg': '密码更新成功！'}, safe=False)
				else:
					return JsonResponse({'success': False, 'msg': '旧密码不正确，请重新输入。'}, safe=False)
			else:
				return JsonResponse({'success': False, 'msg': '用户不存在。'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex.__str__()}, safe=False)

@Check_Login('/login')
def msg_center(request):
	'''消息中心'''
	try:
		msg_list = []
		client_id = request.session.get('client_id',None)
		all_msg = Message.objects.filter(for_all_client=True)
		if all_msg.exists():
			for msg in all_msg:
				msg_dict = {
					'id' : msg.id,
					'title' :msg.title,
					'date_joined': msg.date_joined,
					'client_have_read': True if msg.client_have_read.split(',').count(
						str(client_id))>0 else False
				}
				msg_list.append(msg_dict)
		# client = Client.objects.filter(pk=request.session.get('client_id'))
		# if  client.exists():
		client_msg = Message.objects.filter(client__id=client_id)
		if client_msg.exists():
			for msg in client_msg:
				c_msg_dict = {
					'id': msg.id,
					'title': msg.title,
					'date_joined': msg.date_joined,
					'client_have_read': True if msg.client_have_read.split(',').count(
						str(request.session.get('client_id'))) > 0 else False
				}
				msg_list.append(c_msg_dict)
		msg_list.sort(key=date_joined_sort, reverse=True)
		return render(request,'bms/client_ui/account/msg_center.html',locals())
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

@Check_Login('/login')
def msg_detail(request,msg_id):
	'''消息明细'''
	try:
		if msg_id is not None:
			client_id = request.session.get('client_id')
			find_msg = Message.objects.filter(pk=msg_id)
			if find_msg.exists():
				msg_detail_dict = {
					'title': find_msg.first().title,
					'msg': find_msg.first().msg,
				}
				msg_obj = find_msg.first()
				if msg_obj.client_have_read.split(',').count(
						str(client_id))==0:
					msg_obj.client_have_read += (',' + str(client_id))
					update_dict = {
						'client_have_read':msg_obj.client_have_read
					}
					find_msg.update(**update_dict)
		return render(request,'bms/client_ui/account/msg_detail.html',locals())
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

@Check_Login('/login')
def recharge_page(request):
	'''入金页面'''
	return render(request,'bms/client_ui/account/recharge.html')

@Check_Login('/login')
@check_fund_rule('in')
def recharge(request):
	'''入金操作'''
	try:
		client_id = request.session.get('client_id',None)
		client_name = request.session.get('client_name',None)
		balance_change = request.POST.get('balance_change',None)
		if balance_change is not None and client_id is not None:
			result = offline_client_balance(client_id,'in',Decimal(balance_change),client_name)
			if result:
				return JsonResponse({'success': True, 'msg': '充值申请已提交。'}, safe=False)
		return JsonResponse({'success': False, 'msg': '充值申请参数有误。'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

@Check_Login('/login')
def withdraw_page(request):
	'''出金页面'''
	return render(request,'bms/client_ui/account/withdraw.html')

@Check_Login('/login')
@check_fund_rule('out')
def withdraw(request):
	'''出金操作'''
	try:
		client_id = request.session.get('client_id',None)
		client_name = request.session.get('client_name',None)
		balance_change = request.POST.get('balance_change',None)
		if balance_change is not None and client_id is not None:
			find_client = Client.objects.filter(pk=client_id)
			account_balance = find_client.first().account_balance if find_client.exists() else 0
			if Decimal(balance_change) > account_balance:
				return JsonResponse({'success': False, 'msg': '提现申请数额不能超过账户余额。'}, safe=False)
			result = offline_client_balance(client_id,'out',Decimal(balance_change),client_name)
			if result:
				return JsonResponse({'success': True, 'msg': '提现申请已提交。'}, safe=False)
		return JsonResponse({'success': False, 'msg': '提现申请参数有误。'}, safe=False)
	except Exception as ex:
		print(ex)
		return HttpResponseNotFound(ex)

@Check_Login('/login')
def statement(request):
	'''协议声明'''
	return render(request,'bms/client_ui/account/statement.html')