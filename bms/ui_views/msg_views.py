from bms.tool_kit.view_shortcuts import get_msg_num
from django.shortcuts import render, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse,HttpResponseNotFound
from bms.models import *
from bms.tool_kit.view_shortcuts import get_org_id,get_agency_id,page_helper,msg_have_read

def show_msg_num(request):
	'''显示消息数量'''
	num = get_msg_num(request)
	return JsonResponse({'success': True, 'num': num}, safe=False)

def msg_center(request):
	return render(request,'bms/includes/msg_center.html')

def msg_list(request):
	'''消息列表'''
	try:
		if request.method == 'POST':
			page = request.POST.get("page")
			rows = request.POST.get("rows")
			msg_list = []
			if request.user.identity == 'org':
				msg_list.extend(list(Message.objects.filter(for_all_org=True)))
				msg_list.extend(list(Message.objects.filter(org__id=get_org_id(request))))
			elif request.user.identity=='agency':
				msg_list.extend(list(Message.objects.filter(for_all_agency=True)))
				msg_list.extend(list(Message.objects.filter(org__id=get_agency_id(request))))

			results,total = page_helper(msg_list,rows,page)
			eaList = []
			for msg in results.object_list:
				if request.user.identity == 'org':
					eaList.append({
						'id': msg.id,
						'title': msg.title,
						'msg': msg.msg,
						'type': msg.get_msg_type_display(),
						'operator':msg.operator,
						'date_joined':msg.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
						'have_read': True if msg.org_have_read.split(',').count(
							str(get_org_id(request))) > 0 else False
					})
				elif request.user.identity=='agency':
					eaList.append({
						'id': msg.id,
						'title': msg.get_msg_type_display(),
						'type': msg.msg_type,
						'operator': msg.operator,
						'date_joined': msg.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
						'have_read': True if msg.agency_have_read.split(',').count(
							str(get_agency_id(request))) > 0 else False
					})
			json_data_list = {
				'total': total,
				'rows': eaList
			}
			return JsonResponse(json_data_list, safe=False)
	except Exception as ex:
		print(ex)


def have_read_msg(request):
	'''消息已读'''
	try:
		msg_id = request.POST.get('msg_id')
		msg_have_read(request,msg_id)
		return JsonResponse({'success':True,'msg':'用户添加组成功！'}, safe=False)
	except Exception as ex:
		print(ex)
		return JsonResponse({'success':False,'msg':ex.__str__()}, safe=False)