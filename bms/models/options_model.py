from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from .choices_for_model import OPTION_TYPE,CALL_OR_PUT

def file_path_handler(instance, filename):
	return "file/{id}/{file}".format(id=instance.date_joined.strftime('%Y-%m-%d'), file=filename)  # 保存路径和格式

class Options_File(models.Model):
	'''期权上传文件'''
	file = models.FileField(upload_to=file_path_handler, verbose_name='上传文件')
	op_type = models.CharField(choices=OPTION_TYPE,default='commodity', max_length=32, verbose_name='期权类型')
	effective_date = models.DateField(verbose_name='生效日期')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	def __str__(self):
		return self.file.name

	class Meta:
		ordering = ['-date_joined']
		verbose_name = '期权上传文件'
		verbose_name_plural = '期权上传文件'

class Option_Rate(models.Model):
	'''期权费率表'''
	op_type = models.CharField(choices=OPTION_TYPE,default='commodity', max_length=32, verbose_name='期权类型')
	options_file = models.ForeignKey('Options_File', on_delete=models.CASCADE,
	                        verbose_name='上传文件表外键')
	code = models.CharField(max_length=100,verbose_name='合约代码')
	name = models.CharField(max_length=100,verbose_name='合约名称')
	call_put = models.CharField(choices=CALL_OR_PUT,default='call',max_length=50,verbose_name='期权方向')
	day1 = models.DecimalField(blank=True, null=True,max_digits=12,decimal_places=2, verbose_name='一天')
	day2 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='两天')
	day3 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='三天')
	day4 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='四天')
	day5 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='五天')
	day6 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='六天')
	week1 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='一周')
	week2 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='两周')
	week3 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='三周')
	month1 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='一月')
	month2 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='两月')
	month3 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='三月')
	month4 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='四月')
	month5 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='五月')
	month6 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='六月')
	month7 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='七月')
	month8 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='八月')
	month9 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='九月')
	month10 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='十月')
	month11 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='十一月')
	month12 = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='十二月')
	notional_principal = models.DecimalField(blank=True, null=True, max_digits=12, decimal_places=2, verbose_name='名义本金限制')
	effective_date = models.DateField(verbose_name='生效日期')
	date_joined = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
	operator = models.CharField(max_length=50, blank=True, verbose_name='添加者')

	# def colored_op_type(self):
	# 	if  self.op_type=='commodity':
	# 		return format_html('<span style="color:green">{}</span>',self.get_op_type_display())
	# 	elif self.op_type=='stock':
	# 		return format_html('<span style="color:red">{}</span>',self.get_op_type_display())
	# op_type.short_description = '期权类型'
	#
	# def colored_call_put(self):
	# 	if  self.call_put=='call':
	# 		return format_html('<span style="color:green">{}</span>',self.get_call_put_display())
	# 	elif self.call_put=='put':
	# 		return format_html('<span style="color:red">{}</span>',self.get_call_put_display())
	# call_put.short_description = '期权方向'

	def __str__(self):
		return self.name
	class Meta:
		ordering = ['-date_joined']
		verbose_name = '期权费率表'
		verbose_name_plural = '期权费率表'