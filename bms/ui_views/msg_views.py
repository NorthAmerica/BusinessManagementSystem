from bms.tool_kit.view_shortcuts import get_msg_num
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse,HttpResponseNotFound

def show_msg_num(request):
    '''显示消息数量'''
    num = get_msg_num(request)
    return JsonResponse({'success': True, 'num': num}, safe=False)


def msg_list(request):
    '''消息列表'''
    pass

def msg_detail(request):
    '''消息明细'''
    pass