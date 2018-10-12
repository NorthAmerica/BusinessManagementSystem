WEB_APP_CHOICES = (
		('web', '网页申请'),
		('app', '手机申请'),
		('back','后台录入')
	)

STATUS_CHOICES=(
	('1','已开户待提审'),
	('2','已提审待审核'),
	('3','已审核待入金'),
	('4','已入金待交易'),
	('5','已交易')
)

FUND_TYPE_CHOICES = (
	('online','网银'),
	('offline','线下'),
	('deal','交易'),
	('closing','结算'),
	('rebate','返佣'),
	('raise','加价'),
	('redouble','加倍'),
)

FUND_STATE_CHOICES = (
	 ('in','入金'),
	 ('out','出金'),
	 ('freeze','冻结'),
	 ('unfreeze','解冻'),
	 ('profit','盈利'),
	 ('loss','亏损'),
	)

FUND_STATUS_CHOICES = (
	('none','未审批'),
	('reject','审批未通过'),
	('agree','审核通过'),
)

ORDER_STATUS_CHOICES = (
	('hold','持有'),
	('end','结束'),
)

TEMPLATE_TYPE_CHOICES=(
		('org', '机构模板'),
		('agency', '代理模板'),
	)


BUSINESS_TYPE = (
		('options','期权交易'),
		('margin','融资融券'),
)

OPTION_TYPE = (
		('commodity','商品期权'),
		('stock','个股期权'),
	)

CALL_OR_PUT = (
	('call','看涨'),
	('put','看跌'),
)

OPTION_PATTERN = (
	('virtual','虚值'),
	('flat','平值'),
	('actual','实值'),
)


EVENT_TYPE_CHOICES = (
		('DEBUG','调试'),
		('INFO','信息'),
		('WARNING', '警告'),
		('ERROR', '错误'),
	)

EXCHANGE_TYPE=(
	('enquiry','询价时间设置'),
	('order','下单时间设置'),
	('close','平仓时间设置')
)

DAYS_CHOICE = (
		('Monday', '星期一'),
		('Tuesday', '星期二'),
		('Wednesday', '星期三'),
		('Thursday', '星期四'),
		('Friday', '星期五'),
		('Saturday', '星期六'),
		('Sunday', '星期日'),
	)

IDENTITY_CHOICE=(
		('org','机构管理员'),
		('agency','代理管理员'),
		('admin','后台管理员'),
	)

MSG_TYPE_CHOICE=(
	('public','公共消息'),
	('private','私信'),
)