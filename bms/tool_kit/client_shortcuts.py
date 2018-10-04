from bms.models import *

def get_client_msg_num(client_id):
	try:
		all_msg_num = 0
		all_client_msg = Message.objects.filter(for_all_client=True).exclude(
			client_have_read__contains=str(client_id))
		all_msg_num += all_client_msg.count()

		all_msg_num += Message.objects.filter(client__id=client_id).exclude(
			client_have_read__contains=str(client_id)).count()
		return all_msg_num
	except Exception as ex:
		print(ex)
		return 0
