from decimal import Decimal

from bms.models import *

def get_client_balance(client_id):
	'''获得客户权益'''
	try:
		find_client = Client.objects.filter(pk=client_id)
		if find_client.exists():
			return find_client.first().account_balance
		else:
			return 0
	except Exception as ex:
		print(ex)
		return 0

def change_client_account_balance(client_id,balance_after):
	"""改变客户账户余额"""
	try:
		update_count = Client.objects.filter(pk=client_id).update(account_balance=balance_after)
		if update_count>0:
			return True
		return False
	except Exception as ex:
		print(ex)
		return False

def frozen_client_balance(client_id,frozen_balance):
	"""冻结客户账户金额"""
	try:
		find_client = Client.objects.filter(pk=client_id)
		if find_client.exists():
			client = find_client.first()
			new_account_balance = client.account_balance-frozen_balance
			new_frozen_balance = client.frozen_balance+frozen_balance
			update_count = find_client.update(frozen_balance=new_frozen_balance,account_balance=new_account_balance)
			if update_count>0:
				return True
		return False
	except Exception as ex:
		print(ex)
		return False

def unfrozen_client_balance(client_id,frozen_balance):
	"""解冻客户账户金额"""
	try:
		find_client = Client.objects.filter(pk=client_id)
		if find_client.exists():
			client = find_client.first()
			new_account_balance = client.account_balance + frozen_balance
			new_frozen_balance = client.frozen_balance-frozen_balance
			update_count = find_client.update(frozen_balance=new_frozen_balance,account_balance=new_account_balance)
			if update_count>0:
				return True
		return False
	except Exception as ex:
		print(ex)
		return False

def change_org_account_balance(org_id,balance_after):
	"""改变机构账户余额"""
	try:
		update_count = Organization.objects.filter(pk=org_id).update(account_balance=balance_after)
		if update_count>0:
			return True
		return False
	except Exception as ex:
		print(ex)
		return False

def change_agency_account_balance(agency_id,balance_after):
	"""改变归属账户余额"""
	try:
		update_count = Agency.objects.filter(pk=agency_id).update(account_balance=balance_after)
		if update_count>0:
			return True
		return False
	except Exception as ex:
		print(ex)
		return False

def offline_client_balance(client_id,in_or_out,balance,operator):
	'''客户线下出入金'''
	try:
		find_client = Client.objects.filter(pk=client_id)
		if find_client.exists():
			if in_or_out=='in':
				client = find_client.first()
				old_balance = client.account_balance
				client.account_balance+=balance
				new_balance = client.account_balance
				# Client.objects.filter(pk=client_id).update(account_balance=new_balance)
				fund_dic = {
					'client':client,
					'fund_state':'in',
					'fund_type':'offline',
					'balance_before':old_balance,
					'balance_after':new_balance,
					'balance_change':balance,
					'operator':operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True
			elif in_or_out=='out':
				client = find_client.first()
				old_balance = client.account_balance
				client.account_balance -= balance
				new_balance = client.account_balance
				# Client.objects.filter(pk=client_id).update(**client)
				fund_dic = {
					'client': client,
					'fund_state': 'out',
					'fund_type': 'offline',
					'balance_before': old_balance,
					'balance_after': new_balance,
					'balance_change': balance,
					'operator': operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return False

def offline_org_balance(org_id,in_or_out,balance,operator):
	'''机构线下出入金'''
	try:
		if isinstance(balance,str):
			balance = Decimal(balance)
		find_org = Organization.objects.filter(pk=org_id)
		if find_org.exists():
			if in_or_out=='in':
				org = find_org.first()
				old_balance = org.account_balance
				org.account_balance+=balance
				new_balance = org.account_balance
				# Client.objects.filter(pk=client_id).update(account_balance=new_balance)
				fund_dic = {
					'org':org,
					'fund_state':'in',
					'fund_type':'offline',
					'balance_before':old_balance,
					'balance_after':new_balance,
					'balance_change':balance,
					'operator':operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True,''
			elif in_or_out=='out':
				org = find_org.first()
				if org.account_balance<balance:
					return False,'出金金额不能大于账户余额'
				old_balance = org.account_balance
				org.account_balance -= balance
				new_balance = org.account_balance
				# Client.objects.filter(pk=client_id).update(**client)
				fund_dic = {
					'org': org,
					'fund_state': 'out',
					'fund_type': 'offline',
					'balance_before': old_balance,
					'balance_after': new_balance,
					'balance_change': balance,
					'operator': operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True,''
		else:
			return False,''
	except Exception as ex:
		print(ex)
		return False,ex.__str__()

def offline_agency_balance(agency_id,in_or_out,balance,operator):
	'''归属线下出入金'''
	try:
		if isinstance(balance,str):
			balance = Decimal(balance)
		find_agency = Agency.objects.filter(pk=agency_id)
		if find_agency.exists():
			if in_or_out=='in':
				agency = find_agency.first()
				old_balance = agency.account_balance
				agency.account_balance+=balance
				new_balance = agency.account_balance
				# Client.objects.filter(pk=client_id).update(account_balance=new_balance)
				fund_dic = {
					'agency':agency,
					'fund_state':'in',
					'fund_type':'offline',
					'balance_before':old_balance,
					'balance_after':new_balance,
					'balance_change':balance,
					'operator':operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True
			elif in_or_out=='out':
				agency = find_agency.first()
				if agency.account_balance<balance:
					return False,'出金金额不能大于账户余额'
				old_balance = agency.account_balance
				agency.account_balance -= balance
				new_balance = agency.account_balance
				# Client.objects.filter(pk=client_id).update(**client)
				fund_dic = {
					'agency': agency,
					'fund_state': 'out',
					'fund_type': 'offline',
					'balance_before': old_balance,
					'balance_after': new_balance,
					'balance_change': balance,
					'operator': operator
				}
				Fund_Detail.objects.create(**fund_dic)
				return True
		else:
			return False
	except Exception as ex:
		print(ex)
		return False