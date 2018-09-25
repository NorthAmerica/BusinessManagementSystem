from django.shortcuts import render

def client_list(request):
	return render(request, 'bms/client_config/client_list.html')