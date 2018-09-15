from django.shortcuts import render

def order_list(request):
	return render(request, 'bms/order_config/order_list.html')
