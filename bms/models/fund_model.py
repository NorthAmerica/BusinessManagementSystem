from django.db import models
from django.utils import timezone
from .choices_for_model import CHANGE_TYPE_CHOICES
import time

def random_key():
	'''订单号产生器'''
	return time.strftime('%Y%m%d%H%M%S')+str(int(time.time()*1000))


class Fund_Detail(models.Model):
	"""资金流水明细"""

	order_number = models.CharField(max_length=100,default=random_key,verbose_name='订单号')
	client = models.ForeignKey('Menu',null=True,on_delete=models.SET_NULL, verbose_name='客户')
	change_type = models.CharField(choices=CHANGE_TYPE_CHOICES,default='order',max_length=32,verbose_name='变更类型')
	balance_before = models.DecimalField(null=True,max_digits=12,decimal_places=3, verbose_name='交易前余额')
	balance_after =  models.DecimalField(null=True,max_digits=12,decimal_places=3, verbose_name='交易后余额')
	balance_change = models.DecimalField(null=True,max_digits=12,decimal_places=3, verbose_name='余额变化')
	frozen_balance = models.DecimalField(null=True,max_digits=12,decimal_places=3, verbose_name='交易后冻结余额')
	date_joined = models.DateTimeField(default=timezone.now,verbose_name='操作时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')
	class Meta:
		verbose_name = '资金流水明细'
		verbose_name_plural = '资金流水明细'