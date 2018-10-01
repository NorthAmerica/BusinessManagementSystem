from django.db import models
from django.utils import timezone
from .choices_for_model import OPTION_TYPE,CALL_OR_PUT,OPTION_PATTERN,ORDER_STATUS_CHOICES
import time

def random_key():
	'''订单号产生器'''
	return 'O'+time.strftime('%Y%m%d%H%M%S')+str(int(time.time()*1000))+str(int(time.clock()*1000000))

class Order_Detail(models.Model):
	'''订单明细'''
	serial_number = models.CharField(max_length=100, default=random_key, verbose_name='订单流水号')
	client = models.ForeignKey('Client', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='客户')
	org = models.ForeignKey('Organization', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='机构')
	agency = models.ForeignKey('Agency', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='归属')
	option_type = models.CharField(choices=OPTION_TYPE,max_length=100,blank=True, null=True,verbose_name='期权种类')
	call_put = models.CharField(choices=CALL_OR_PUT,max_length=100,blank=True,null=True,verbose_name='期权类型')
	option_pattern = models.CharField(choices=OPTION_PATTERN,max_length=100,blank=True,null=True,verbose_name='期权模式')
	option_code = models.CharField(blank=True, null=True,max_length=100,verbose_name='商品代码')
	option_name = models.CharField(blank=True, null=True,max_length=100,verbose_name='商品名称')
	option_rate = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='期权费率')
	order_number = models.IntegerField(blank=True,null=True, verbose_name='下单手数')
	order_price = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='下单价格')
	close_price = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='结算价格')
	position_profit_loss = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='持仓盈亏')
	closing_profit_loss = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='平仓盈亏')
	settlement_profit_loss = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='结算盈亏')
	today_profit_loss = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='今日盈亏')
	exercise_day = models.IntegerField(blank=True,null=True, verbose_name='行权天数')
	notional_principal = models.DecimalField(blank=True,null=True,max_digits=12,decimal_places=2, verbose_name='名义本金')
	status = models.CharField(choices=ORDER_STATUS_CHOICES,max_length=100,blank=True,null=True,verbose_name='订单状态')
	date_closing = models.DateTimeField(blank=True, null=True, verbose_name='结算日期')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='下单时间')
	operator = models.CharField(max_length=50, blank=True, null=True, verbose_name='添加者')

	def __str__(self):
		return self.serial_number

	class Meta:

		verbose_name = '订单明细'
		verbose_name_plural = '订单明细'