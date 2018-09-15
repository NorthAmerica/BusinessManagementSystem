from django.shortcuts import render

def funds_list(request):
	return render(request, 'bms/funds_config/funds_list.html')