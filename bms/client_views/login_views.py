from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse

def login(request):
	return render(request,'bms/client_ui/login.html')

def login_check(request):
	try:
		if request.method == 'POST':
			username = request.POST.get('username')
			pwd = request.POST.get('password')
			return JsonResponse({'success': True, 'msg': ''})
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex})


def register(request):
	return render(request,'bms/client_ui/register.html')

def reg_check(request):
	try:
		if request.method == 'POST':
			code = request.POST.get('code')
			user_tel = request.POST.get('tel')
			pwd = request.POST.get('pwd')
			return JsonResponse({'success': True, 'msg': ''})
	except Exception as ex:
		print(ex)
		return JsonResponse({'success': False, 'msg': ex})