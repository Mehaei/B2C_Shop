from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from .. models import *
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator

@permission_required('myadmin.show_order',raise_exception = True)

# 订单列表
def orderlist(request):
	# keywords = request.GET.get('keywords',None)
	# orderlist = {'待付款':1,'待发货':2,'待收货':3,'待评价':4,'已取消':5}
	# if keywords:
	# 	db = Order.objects.filter(stauts__contains=orderlist.get(keywords,'aa'))
	# else:	
	types = request.GET.get('types',None)
	if types:
		if types == '1':
			db = Order.objects.filter(stauts = 1)
		elif types == '2':
			db = Order.objects.filter(stauts = 2)
		elif types == '3':
			db = Order.objects.filter(stauts = 3)
		elif types == '4':
			db = Order.objects.filter(stauts = 4)
		elif types == '5':
			db = Order.objects.filter(stauts = 5)
	else:

		db = Order.objects.all()	
	# 数据分页	
	# 实例化分页类
	paginator = Paginator(db,5)

	# 当前页码
	p = int(request.GET.get('p',1))
	#根据当前页码获取当前页码显示的数据
	db = paginator.page(p)


	return render(request,'admin/order/orderlist.html',{"orderlist":db})
	# return HttpResponse('123')
@permission_required('myadmin.show_order',raise_exception = True)

# 订单详情
def orderinfo(request,oid):
	db = Order.objects.get(id = oid)
	# print(db)
	context = {'order':db}
	return render(request,'admin/order/orderinfo.html',context)
@permission_required('myadmin.edit_order',raise_exception = True)

# 修改订单状态
def orderstatus(request):

	oid = request.GET['oid']

	vall = request.GET['vall']

	db = Order.objects.get(id = oid)
	db.stauts = vall
	db.save()

	return HttpResponse('6')