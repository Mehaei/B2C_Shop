from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from .. models import *
from django.db.models import Q	
from . views import addpic
from django.contrib.auth.decorators import permission_required

@permission_required('myadmin.insert_goods',raise_exception = True)
# 商品添加页
def goodsadd(request):
	from . typeviews import GetTypesAll

	context = {'info':GetTypesAll()}
	# return HttpResponse('goodsadd')
	return render(request,'admin/goods/add.html',context)

@permission_required('myadmin.insert_goods',raise_exception = True)
# 商品执行添加
def goodsinsert(request):
	
	# print(request.POST['typeid'])
	if not request.FILES.get('pic',None):
		return HttpResponse('<script>alert("请选择上传图片");location.href="'+reverse('admin_goods_add')+'"</script>')
	try:
		db = Goods()
		db.typeid = Types.objects.get(id = request.POST['typeid'])
		db.title  = request.POST['title']
		db.price = request.POST['price']
		db.storage = request.POST['storage']
		db.info = request.POST['info']
		db.pic = addpic(request)
		db.save()
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('admin_goods_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("添加失败");location.href="'+reverse('admin_goods_add')+'"</script>')

@permission_required('myadmin.show_goods',raise_exception = True)
# 商品列表页
def goodslist(request):
	orr = request.GET.get('orr',None)

	types = request.GET.get('type',None)
	keywords = request.GET.get('keywords',None)
	goodslist = {'新品':1,'热销':2,'下架':3}
	if types:
		if types == 'all':
			db = Goods.objects.filter(Q(title__contains=keywords)|Q(id__contains=keywords)|Q(price__contains=keywords)|Q(status__contains=goodslist.get(keywords,'a')))
		elif types == 'title':
			db = Goods.objects.filter(title__contains=keywords)
		elif types == 'status':
			db = Goods.objects.filter(status__contains=goodslist.get(keywords,'a'))
	# print(keywords)

	elif orr == 'up':
		db = Goods.objects.order_by('price')
	elif orr == 'down':
		db = Goods.objects.order_by('-price')
	
	# aa = Goods.objects.order_by('price')
	# print(aa[0].price)
	else:
		db = Goods.objects.all()
	# print(db)
	# 数据分页
	from django.core.paginator import Paginator
	# 实例化分页类
	paginator = Paginator(db,5)

	# 当前页码
	p = request.GET.get('p',1)
	#根据当前页码获取当前页码显示的数据
	db = paginator.page(p)

	context = {'glist':db}
	return render(request,'admin/goods/list.html',context)
	# return HttpResponse('goodslist')

@permission_required('myadmin.edit_goods',raise_exception = True)
# 商品修改页
def goodsedit(request,tid):
	# print(tid)
	db = Goods.objects.get(id = tid)
	ob = Types.objects.all()
	# ob = Types.objests.get(id = db.typeid)
	# print(db.typeid.id)
	# print(ob)
	# return HttpResponse('goodsedit')
	return render(request,'admin/goods/edit.html',{'glist':db,'tlist':ob})

@permission_required('myadmin.edit_goods',raise_exception = True)
# 商品执行修改
def goodsupdate(request):
	try:
		db = Goods.objects.get(id =request.POST['tid'])
		db.title = request.POST['title']
		db.price = request.POST['price']
		db.storage = request.POST['storage']
		db.info = request.POST['info']
		db.typeid = Types.objects.get(id = request.POST['typeid'])
		if not request.FILES.get('pic',None):
			db.pic = db.pic
		else:
			db.pic = addpic(request)
		db.save()
		return HttpResponse('<script>alert("修改成功");location.href="'+reverse('admin_goods_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("修改失败");location.href="'+reverse('admin_goods_list')+'"</script>')

	# return HttpResponse('开始执行修改吧')

@permission_required('myadmin.edit_goods',raise_exception = True)
# 修改商品状态
def goodsstatus(request):
	db = Goods.objects.get(id = request.GET['uid'])
	# print(request.GET['status'])
	db.status = request.GET['status']
	db.save()
	return HttpResponse('lll')

@permission_required('myadmin.del_goods',raise_exception = True)	
# 删除商品
def goodsdel(request):
	try:
		db = Goods.objects.get(id = request.GET['tid'])
		# db.delete()
		# print(type(db.status))
		if db.status == 3:
			db.delete()
			return HttpResponse('0')
		else:
			return HttpResponse('1')
	except:
		return HttpResponse('1')