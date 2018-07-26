from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from myadmin.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
# Create your views here.

def emailss(request):
	
 
	send_mail('Subject here', '王八蛋,您好', 'mswyf1204@qq.com',['2310649541@qq.com'], fail_silently=False)

	return HttpResponse('132')
# 为每个页面的导航栏传送数据
def gettype():

	data = Types.objects.exclude(pid=0)[:6]
	# for i in data:
	# 	i.sub = Types.objects.filter(pid = i.id)

	return data

#首页
def index(request):
	# 查询所有的顶级分类
	data = Types.objects.filter(pid=0)
	# 循环遍历每个顶级对象
	for x in data:
		# 为每个顶级对象添加一个键为sub　值为对应id的对象
		x.sub = Types.objects.filter(pid = x.id)
		#循环遍历每个顶级对象的键为sub的值（现在每个sub的值为一个对象）
		for y in x.sub:
			#为每个顶级的sub中的sub添加一个对应id　的对象
			y.sub = Goods.objects.filter(typeid = y.id)[:8]
	# print(data[1].sub[0].sub[0].title)
	# print(data)
	context = {'typelist':gettype(),'data':data}

	return render(request,'home/index.html',context)
	# return HttpResponse('首页')

# 用户注册页
def register(request):

	# 判断提交方式
	if request.method == 'GET':
		return render(request,'home/register.html')
	elif request.method == 'POST':
		# 判断用户名是否存在
		res = Users.objects.filter(username=request.POST['username']).exists()

		# print(res)
		if res:
			#如果存在返回提醒 
			return HttpResponse('<script>alert("用户名已存在");location.href="'+reverse('register')+'"</script>')
		else:
			# 将用户信息保存到数据库
			db = Users()
			db.username = request.POST['username']
			db.email = request.POST['email']
			db.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
			db.save()
			# 将session写入用户信息
			request.session['VipUser'] = {'name':db.username,'pic':db.picurl,'uid':db.id}
			# 注册成功跳回首页
			return HttpResponse('<script>alert("注册成功");location.href="/"</script>')

# 用户登录页
def login(request):
	if request.method == 'GET':
		return render(request,'home/login.html')

	elif request.method == 'POST':
		# 判断验证码是否输入正确
		if request.POST['vcode'].lower() != request.session['verifycode'].lower():
			# 如不正确返回登录页
			return HttpResponse('<script>alert("验证码不正确");location.href="'+reverse('login')+'"</script>')
		# 获取输入的用户名的整条数据　如不存在则为空
		db = Users.objects.filter(username=request.POST['username'])
		# 如果存在 则进一步判断
		if db:
			db = db[0]
			# 判断密码是否正确
			if check_password(request.POST['password'],db.password):
				# 将用户信息写入session
				request.session['VipUser'] = {'name':db.username,'pic':db.picurl,'uid':db.id}
				request.session.set_expiry(0)
				return HttpResponse('<script>alert("登录成功");location.href="/"</script>')
	# 不管那种情况不符合判断条件则返回
	return HttpResponse('<script>alert("用户名不存在或密码不正确");location.href="'+reverse('login')+'"</script>')

# 用户忘记密码页
def forget(request):

	return render(request,'home/forget.html')

# 验证忘记密码用户账户信息
def forget_edit(request):

	ob = Users.objects.filter(email = request.POST['email'])
	# print(ob[0].id)
	# 如果邮箱不存在，则返回错误
	if not ob:
		return HttpResponse('<script>alert("邮箱不存在,请输入已注册邮箱地址");location.href="'+reverse('forget')+'"</script>')
	# 存在则跳转到设置新密码的页面
	else:
		return HttpResponse('<script>alert("验证成功，请设值新密码");location.href="forgetnew/'+str(ob[0].id)+'"</script>')

# 设置新密码页面
def forgetnew(request,uid):

	db = Users.objects.get(id=uid)
	# print(db)
	return render(request,'home/forgetnew.html',{'db':db})
	# return HttpResponse('恭喜你，离成功又近了一步')
# 
# 执行新设置的密码修改
def forget_new_insert(request):

	db = Users.objects.get(id = request.POST['uid'])
	db.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
	db.save()
	return HttpResponse('<script>alert("账户修改成功，请登录");location.href="'+reverse('login')+'"</script>')

# 退出登录
def loginout(request):

	del request.session['VipUser']
 
	return HttpResponse('<script>alert("注销成功");location.href="/"</script>')

# 列表页
def list(request,tid):
	
	db = Types.objects.get(id = tid)

	if db.pid == 0:
		data = db

		data.sub = Types.objects.filter(pid = db.id)
		# print(data.sub)
		ids = []
		for i in data.sub:
			# print(i.id)
			ids.append(i.id)
		data.goods = Goods.objects.filter(typeid__in=ids)
	else:
		# 获取负极对象
		data = Types.objects.get(id = db.pid)

		# 获取当前自雷的商品信息
		data.goods = Goods.objects.filter(typeid = db.id)

		# 获取所有的统计信息，包括当前类
		data.sub = Types.objects.filter(pid = db.pid)

		# 给fata数据追加一个obj对象
		data.obj = db
	# print( db.id)
	context = {'typelist':gettype(),'data':data}
	return render(request,'home/list.html',context)

# 详情页
def info(request,gid):
	# print(gid)
	db = Goods.objects.get(id = gid)
	context = {'typelist':gettype(),'ginfo':db}
	return render(request,'home/info.html',context)
	# return HttpResponse(gid)

# 添加商品到购物车
def cartadd(request):
	try:
		# 获取商品的ｉｄ和数量
		gid = request.GET['gid']
		num = int(request.GET['num'])

		# 获取ｓｅｓｓｉｏｎ中的数据
		data = request.session.get('cart',{})
		# 判断该商品是否在ｓｅｓｓｉｏｎ当中
		# 如果在　就直接将原有的数量加上现在的的数量
		if gid in data:
			data[gid]['num'] += num
		else:
			# 如果不在则查询该商品的详细信息
			goods = Goods.objects.get(id = gid)
			# 并加入到ｓｅｓｓｉｏｎ中
			data[gid] = {'id':gid,'title':goods.title,'price':str(goods.price),'pic':goods.pic,'num':num}
		# 将结果放入ｓｅｓｓｉｏｎ中
		request.session['cart'] = data
		return JsonResponse({'code':0,'tsy':'加入购物车成功'})
	except:
		return JsonResponse({'code':1,'tsy':'加入购物车成功'})

# 购物车列表
def cartlist(request):

	# return HttpResponse('123')
	context = {'typelist':gettype()}

	return render(request,'home/cartlist.html',context)
	
# 清空购物车
def cartclear(request):
	request.session['cart'] = {}

	return HttpResponse('<script>location.href="/cartlist/"</script>')

# 删除商品
def delone(request,gid):
	# 找到删除的商品　并删除
	data = request.session['cart']
	
	del data[gid]

	request.session['cart'] = data
	
	return HttpResponse('<script>location.href="/cartlist/"</script>')

# 商品数量减少操作
def subtract(request):
	# 获取进行操作的商品ｉｄ和数量
	gid = request.GET['gid']
	num = int(request.GET['num'])
	# print(gid)

	data = request.session['cart']
	# 判断商品数量如果大于１　则进行减１操作　反之则等于１
	if data[gid]['num'] > 1:

		data[gid]['num'] = int(data[gid]['num']) -1
	else:

		data[gid]['num'] = 1
		# 将数据写入ｓｅｓｓｉｏｎ
	request.session['cart'] = data
	# 算出商品的总价带入到页面
	total = int(data[gid]['num']) * float(data[gid]['price'])
	# 保留两位小数
	context = {'num':data[gid]['num'],'total':'%.2f'%total}
	return JsonResponse(context,safe=False)

# 商品数量增加操作
def subadd(request):
	gid = request.GET['gid']
	num = int(request.GET['num'])
	# print(gid)

	data = request.session['cart']
	
	data[gid]['num'] = int(data[gid]['num']) + 1

	request.session['cart'] = data

	total = int(data[gid]['num']) * float(data[gid]['price'])

	context = {'num':data[gid]['num'],'total':'%.2f'%total}
	return JsonResponse(context,safe=False)

# 确认订单
def order_confirm(request):
	# 判断提交方式
	if request.method == 'GET':
		# 获取用户选择的商品
		ids = request.GET['ids'].split(',')

		# session中读取购物车信息
		cartdata = request.session['cart']
		# 定义一个新的字典　存放勾选的商品
		orderdata = {}
		# 遍历所有购物车的商品，并将勾选的商品加入到新的字典
		for i in cartdata:
			if i in ids:
				orderdata[i] = cartdata[i]

		request.session['order'] = orderdata
		# 获取选中的个数
		llen = len(orderdata)
		total = 0
		# 计算选中商品的总价
		for v in orderdata:

			total += int(orderdata[v]['num']) * float(orderdata[v]['price'])
		# 查询登录用户的收货地址
		address = Address.objects.filter(uid = request.session['VipUser']['uid'])
		# print(address['uname'])
		context = {"typelist":gettype(),"a":1,'address':address,'llen':llen,'total':'%.2f'%total}

		return render(request,'home/orderconfirm.html',context)
	elif request.method == 'POST':
		# 将用户信息写入到库中
		db = Address()
		db.uid = Users.objects.get(id = request.session['VipUser']['uid'])
		db.uname = request.POST['uname']
		db.uphone = request.POST['uphone']
		db.uaddr = request.POST['uaddr']
		# 获取用户默认地址的勾选情况
		stu = request.POST.get('status',0)
		# 如果等于１　则代表用户勾选了将新添加的地址设置为新的默认地址
		if stu == '1':
			#获取所有地址为默认的地址
			addr = Address.objects.filter(status = 1,uid = request.session['VipUser']['uid'])
			# 遍历所有地址　并将地址状态改为不是默认的状态
			for x in addr:
				x.status = 0
				x.save()
		db.status = stu
		db.save()
		return HttpResponse('<script>alert("地址添加完成");location.href="/order/confirm/?ids='+request.GET['ids']+'"</script>')
		# return render(request,'home/orderconfirm.html')

# 立即购买
def order_confirmm(request,gid):

	db = Goods.objects.get(id = gid)

	val = request.POST['num']

	total = int(val) * float(db.price)

	address = Address.objects.filter(uid = request.session['VipUser']['uid'])
	
	context = {"typelist":gettype(),'ginfo':db,'val':val,"a":0,'address':address,'llen':1,'total':'%.2f'%total}
	
	return render(request,'home/orderconfirm.html',context)



# 生成订单
def order_create(request):
	# 获取订单信息
	data = request.session['order']
	# 声明统计总数和总价的变量
	totalnum = 0
	totalprice = 0
	# 遍历订单中的信息　统计总价和总量
	for i in data:
		totalnum += data[i]['num']
		totalprice += data[i]['num'] * float(data[i]['price'])

	# print(request.POST.get('addressid'))
	# 生成订单信息
	db = Order()
	db.uid = Users.objects.get(id = request.session['VipUser']['uid'])
	db.address = Address.objects.get(id = request.POST.get('addressid'))
	db.totalprice = totalprice
	db.totalnum = totalnum
	db.stauts = 1
	db.save()

	# 读取购物车中的数据
	cart = request.session['cart']

	# 写入订单详情页
	for i in data:
		# print(data[i])
		orderinfo = OrderInfo()
		# 订单详情中的ｉｄ就是刚生成的订单信息对象
		orderinfo.orderid = db
		goods = Goods.objects.get(id = i)
		orderinfo.gid = goods
		orderinfo.num = data[i]['num']
		orderinfo.price = data[i]['price']
		# print(data[i]['price'])
		orderinfo.save()
		# print(totalnum,totalprice)

		# 增加购买量
		goods.num += data[i]['num']
		# 减少库存量
		goods.storage -= data[i]['num']

		# 删除购物车中的数据
		del cart[i]

	# 清除订单中的数据
	request.session['order'] = {}

	# 更新购物车
	request.session['cart'] = cart

	return render(request,'home/orderbuy.html',{'typelist':gettype,'order':db})

# 我的订单页
def myorder(request):

	
	status = request.GET.get('status',None)
	if status:
		if status == 'sone':
			db = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 1)
			# print('sone')
		elif status == 'stwo':
			db = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 2)
			# print('stwo')
		elif status == 'stree':
			# print('stree')
			db = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 3)

		elif status == 'sfour':
			# print('sfour')
			db = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 4)
		elif status == 'all':
			
			db = Order.objects.filter(uid = request.session['VipUser']['uid'])
	else:
		db = Order.objects.filter(uid = request.session['VipUser']['uid'])
	# 读取登录用户的订单
	# print(db)
	# return HttpResponse('234')
	return render(request,'home/myorder.html',{'order':db,'typelist':gettype()})

# 用户付款成功后　修改订单状态
def edit_order_status(request):
	try:
		uid = request.GET['uid']
		order = Order.objects.get(id = uid)
		order.stauts = 2
		order.save()
		# 成功返回　０　
		return HttpResponse(0)
	except:
		# 失败返回　１
		return HttpResponse(1)

# 个人中心
def my_center(request):
	db = Users.objects.get(id = request.session['VipUser']['uid'])

	norder = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 1,).count()

	uorder = Order.objects.filter(uid = request.session['VipUser']['uid'],stauts = 2).count()
	print(norder,uorder)
	context = {'typelist':gettype(),'db':db,'norder':norder,'uorder':uorder}

	return render(request,'home/mycenter.html',context)

# 订单详情
def order_info(request,uid):

	db = Order.objects.filter(id = uid)
	return render(request,'home/orderinfo.html',{'order':db,'typelist':gettype()})

# 地址管理
def address_manage(request):
	db = Address.objects.filter(uid = request.session['VipUser']['uid'])
	# print(request.session['VipUser']["uid"])
	# print(db)
	return render(request,'home/amanage.html',{'order':db,'typelist':gettype()})

# 地址修改
def address_edit(request):
	try:
	# 	# 将用户信息写入到库中
		db = Address.objects.get(id = request.POST['tid'])
		db.uid = Users.objects.get(id = request.session['VipUser']['uid'])
		db.uname = request.POST['uname']
		db.uphone = request.POST['uphone']
		db.uaddr = request.POST['uaddr']
		# 获取用户默认地址的勾选情况
		stu = request.POST.get('status',0)
		# 如果等于１　则代表用户勾选了将新添加的地址设置为新的默认地址
		if stu == '1':
			#获取所有地址为默认的地址
			addr = Address.objects.filter(status = 1,uid = request.session['VipUser']['uid'])
			# 遍历所有地址　并将地址状态改为不是默认的状态
			for x in addr:
				x.status = 0
				x.save()
		else:
			db.status = 0
		db.status = stu
		db.save()
		return HttpResponse('<script>alert("地址修改完成");location.href="/address/manage/"</script>')
	# 	# return render(request,'home/orderconfirm.html')
	except:
		return HttpResponse('<script>alert("地址修改失败");location.href="/address/manage/"</script>')

# 地址添加
def address_add(request):
	try:
	# 	# 将用户信息写入到库中
		db = Address()
		db.uid = Users.objects.get(id = request.session['VipUser']['uid'])
		db.uname = request.POST['uname']
		db.uphone = request.POST['uphone']
		db.uaddr = request.POST['uaddr']
		# 获取用户默认地址的勾选情况
		stu = request.POST.get('status',0)
		# 如果等于１　则代表用户勾选了将新添加的地址设置为新的默认地址
		if stu == '1':
			#获取所有地址为默认的地址
			addr = Address.objects.filter(status = 1,uid = request.session['VipUser']['uid'])
			# 遍历所有地址　并将地址状态改为不是默认的状态
			for x in addr:
				x.status = 0
				x.save()
		db.status = stu
		db.save()
		return HttpResponse('<script>alert("地址添加完成");location.href="/address/manage/"</script>')
	# 	# return render(request,'home/orderconfirm.html')
	except:
		return HttpResponse('<script>alert("地址添加失败");location.href="/address/manage/"</script>')

# 删除地址
def address_del(request,tid):
	try:
		db = Address.objects.get(id = tid)
		db.delete()
		return HttpResponse('<script>location.href="/address/manage/"</script>')
	# 	# return render(request,'home/orderconfirm.html')
	except:
		return HttpResponse('<script>alert("地址删除失败");location.href="/address/manage/"</script>')

# 个人信息修改
def mycenter_edit(request):
	try:
		uid = request.POST['tid']
		# print(uid)
		db = Users.objects.get(id = uid)
		db.username = request.POST['name']
		db.phone = request.POST['phone']
		db.email = request.POST['email']
		db.save()
		# 清除原session　并写入新的session
		del request.session['VipUser']
		request.session['VipUser'] = {'name':db.username,'pic':db.picurl,'uid':db.id}
		# 关闭浏览器　session失效
		request.session.set_expiry(0)
		return HttpResponse('<script>alert("修改成功");location.href="/mycenter/"</script>')
	# 	# return render(request,'home/orderconfirm.html')
	except:
		return HttpResponse('<script>alert("修改失败");location.href="/mycenter/"</script>')

# 默认地址修改
def order_status_edit(request):
	# 获取用户状态为１的地址
	addr = Address.objects.filter(status = 1,uid = request.session['VipUser']['uid'])
	# 遍历默认地址　将状态该为０
	for x in addr:
		x.status = 0
		x.save()
	
	db = Address.objects.get(id = request.GET['gid'])
	#获取所有地址为默认的地址
	db.status = 1
	db.save()
	return HttpResponse(1)

# 取消 删除订单
def order_del(request):
	# print(request.GET['gid'])
	db = Order.objects.get(id = request.GET['gid'])
	db.delete()
	return HttpResponse('0')