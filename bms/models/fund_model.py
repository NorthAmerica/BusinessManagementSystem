from django.db import models
from django.utils import timezone
from .choices_for_model import FUND_STATE_CHOICES,FUND_TYPE_CHOICES,FUND_STATUS_CHOICES
import time

def random_key():
	'''订单号产生器'''
	return 'F'+time.strftime('%Y%m%d%H%M%S')+str(int(time.time()*1000))+str(int(time.clock()*1000000))


class Fund_Detail(models.Model):
	"""资金流水明细"""
	serial_number = models.CharField(max_length=100,default=random_key,verbose_name='资金流水号')
	client = models.ForeignKey('Client',blank=True,null=True,on_delete=models.SET_NULL, verbose_name='客户')
	org = models.ForeignKey('Organization',blank=True,null=True,on_delete=models.SET_NULL, verbose_name='机构')
	agency = models.ForeignKey('Agency',blank=True,null=True,on_delete=models.SET_NULL, verbose_name='归属')
	order = models.ForeignKey('Order_Detail',blank=True,null=True,on_delete=models.SET_NULL, verbose_name='订单号')
	fund_state = models.CharField(choices=FUND_STATE_CHOICES,default='in',blank=True,null=True,max_length=32,verbose_name='资金类型')
	fund_type = models.CharField(choices=FUND_TYPE_CHOICES,default='online',blank=True,null=True,max_length=32,verbose_name='资金渠道')
	fund_audit = models.CharField(choices=FUND_STATUS_CHOICES,default='none',blank=True,null=True,max_length=32,verbose_name='资金审核')
	auditor = models.CharField(max_length=50, blank=True, verbose_name='审核者')
	audit_time = models.DateTimeField(blank=True,null=True,verbose_name='审核时间')
	balance_before = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='交易前余额')
	balance_after =  models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='交易后余额')
	balance_change = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='交易金额')
	# frozen_balance = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='冻结金额',help_text='在冻结解冻操作时使用')
	date_joined = models.DateTimeField(default=timezone.now,verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True,null=True, verbose_name='添加者')

	def __str__(self):
		return self.serial_number

	class Meta:
		verbose_name = '资金流水明细'
		verbose_name_plural = '资金流水明细'