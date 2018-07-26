from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from .. models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import permission_required
from django.db.models import Q	

# 后台首页


	# return HttpResponse('OK')
# # 登录验证
# def logintest(request):
# 	# 获取输入的账号和密码
# 	aadminname = request.POST['adminname']
# 	apassword = request.POST['password']
# 	# 查询数据库的账号和面膜
# 	data =  Admin.objects.filter(adminname=aadminname)
# 	date = 	Admin.objects.filter(password = apassword)
# 	# 便利查出来的对象和取出对应的ｉｄ
# 	for i in data:

# 		print(type(i.id))
# 	for v in date:
# 		print(v.id)
# 		# 判断账号和密码是否为一条数据和是否存在
# 		if i.id == v.id:
# 			return HttpResponse('<script>alert("大哥，欢迎回家");location.href="'+reverse('admin_index')+'"</script>')
# 	return HttpResponse('<script>alert("账户不存在或密码不正确");location.href="'+reverse('admin_login')+'"</script>')


# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(104, 125), random.randrange(
        0, 255),255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')




 # 后台首页
# Create your views here.

# 首页数据显示
def base_qeust(request):
	ad = Admin.objects.count()
	bd = Users.objects.count()
	cd = Types.objects.count()
	dd = Goods.objects.count()
	print(cd)
	# return JsonResponse(ad)
	return JsonResponse({'ad':ad,'bd':bd,'cd':cd,'dd':dd})
	# return HttpResponse(bd)






#后台管理员添加
def admin_add(request):

	# return HttpResponse('ok')
	return render(request,'admin/adminuser/add.html')

# 后台管理员执行添加
def admin_insert(request):
	try:
		db = Admin()
		db.adminname = request.POST['username']
		db.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
		db.save()
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('admin_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("添加失败");location.href="'+reverse('admin_add')+'"</script>')
# 后台管理员列表
def admin_list(request):
	
	db = Admin.objects.all()


	return render(request,'admin/adminuser/list.html',{'alist':db})
# 修改后台管理员账号状态
def admin_status(request):

	db = Admin.objects.get(id = request.GET.get('uid'))
	# print(db)
	db.status = int(request.GET['status'])
	db.save()
	return HttpResponse("123")
# 执行删除管理员
def admin_del(request,tid):

	db = Admin.objects.get(id=tid)
	db.delete()
	return HttpResponse('<script>alert("删除成功");location.href="'+reverse('admin_list')+'"</script>')


# 后台首页
def adminindex(request):

	return render(request,'admin/index.html')

@permission_required('myadmin.insert_users',raise_exception = True)
# 会员添加
def useradd(request):

	return render(request,'admin/user/add.html')

@permission_required('myadmin.insert_users',raise_exception = True)
# 执回会员添加
def userinsert(request):

	pic =  addpic(request)
	# 判断图片格式是否正确
	if not pic:
		return HttpResponse('<script>alert("图片格式不正确");location.href="'+reverse('admin_user_add')+'"</script>')
	try:
		db = Users()
		db.username = request.POST.get('username')
		db.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
		db.email = request.POST.get('email')
		db.age = request.POST.get('age')
		db.phone = request.POST.get('phone')
		db.sex = request.POST.get('sex')
		db.picurl = pic
		db.save()
		# return HttpResponse('<script>alert("tianjiachenggong ")</script>')
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('admin_user_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("添加失败");location.href="'+reverse('admin_user_add')+'"</script>')

@permission_required('myadmin.show_users',raise_exception = True)
# 会员列表页
def userlist(request):
	
	# 搜索条件
	types = request.GET.get('type',None)
	# 搜索参数
	keywords = request.GET.get('keywords','')
	# 定义列表
	statuslist = {'正常':0,'禁用':1}

	# 如果有搜索条件
	if types:
		if types == 'all':
			# return HttpResponse('全部条件搜索')
					
			data = Users.objects.filter(Q(username__contains=keywords)|Q(email__contains=keywords)|Q(phone__contains=keywords)|Q(age__contains=keywords)|Q(sex__contains=keywords)|Q(addtime__contains=keywords)|Q(status__contains=statuslist.get(keywords,'aa'))).exclude(status=3)
		elif types == 'username':
			# return HttpResponse('用户名搜索')
			data = Users.objects.filter(username__contains=keywords).exclude(status=3)
		elif types == 'email':
			data = Users.objects.filter(email__contains=keywords).exclude(status=3)
			# return HttpResponse('邮箱搜索')
		elif types == 'phone':
			data = Users.objects.filter(phone__contains=keywords).exclude(status=3)
			# return HttpResponse('手机号搜索')
		elif types == 'age':
			data = Users.objects.filter(age__contains=keywords).exclude(status=3)
			# return HttpResponse('年龄搜索')
		elif types == 'sex':
			data = Users.objects.filter(sex__contains=keywords).exclude(status=3)
			# return HttpResponse('性别搜索')
		elif types == 'addtime':
			data = Users.objects.filter(addtime__contains=keywords).exclude(status=3)
			# return HttpResponse('创建时间搜索')
		elif types == 'status':
			data = Users.objects.filter(status__contains=statuslist.get(keywords,'aa')).exclude(status=3)
			# return HttpResponse('账号状态搜索')
	# 没有搜索条件
	else:

		data = Users.objects.exclude(status=3)

		# 数据分页
	from django.core.paginator import Paginator
	# 实例化分页类
	paginator = Paginator(data,10)

	# 当前页码
	p = request.GET.get('p',1)
	#根据当前页码获取当前页码显示的数据
	userlist = paginator.page(p) 

	# print(num)
	context = {'info':userlist}
	# print(db)
	# return HttpResponse('跳转成功，可执行下一步')
	return render(request,'admin/user/list.html',context)

@permission_required('myadmin.edit_users',raise_exception = True)
# 会员修改页
def useredit(request,uid):
	db = Users.objects.get(id=uid)
	# print(db.id)
	
	return render(request,'admin/user/edit.html',{'info':db})
	# return HttpResponse('跳转成功，可执行下一步')


@permission_required('myadmin.edit_users',raise_exception = True)
# 执行修改
def userupdate(request):
	try:
		uid = int(request.POST['uid'])
		# uid = request.POST.get('username')
		db = Users.objects.get(id=uid)
		# print(type(uid))
		db.username = request.POST['username']
		db.email = request.POST['email']
		db.phone = request.POST['phone']
		db.age = request.POST['age']
		db.sex = request.POST['sex']
	     # 判断是否有文件上传
		if request.FILES.get('pic'):
	        # 判断是否使用的默认图
			if db.picurl != '/static/pics/default/defaultt.jpg':
				import os
	            #不是默认头像,则执行删除
				os.remove('.'+db.picurl) 
	        # 上传新的头像
			db.picurl = addpic(request)
		db.save()
		return HttpResponse('<script>alert("修改成功");location.href="'+reverse('admin_user_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("修改失败");location.href="'+reverse('admin_user_list')+'"</script>')

@permission_required('myadmin.del_users',raise_exception = True)

# 执行修改用户状态
def userdel(request):
	try:
		tid = request.GET.get('tid')
		db = Users.objects.get(id=tid)
		db.status = 3
		db.save()
		print(db)
		return HttpResponse('0')
	except:
		return HttpResponse('1')

@permission_required('myadmin.del_users',raise_exception = True)
# 点击下拉框修改用户状态,
def userstatus(request):
	# 获取点击的用户ＩＤ
	db = Users.objects.get(id=request.GET['uid'])
	# 获取点击的用户的状态
	db.status = int(request.GET['status'])
	# print(db)
	db.save()

	return HttpResponse('')

# 添加图片函数
def addpic(request):
	# global test
	# 获取用户上传图片
	mypic = request.FILES.get('pic')
	# 如果没有上传　则使用默认图片
	if not mypic:
		return '/static/pics/default/defaultt.jpg'
	# print(mypic)
	import time
	# 制作图片名
	filename = str(time.ctime())
	# 获取原文件后缀
	hz = mypic.name.split('.').pop()
	# 制定上传图片格式
	arr = ['jpg','png','gif']
	# 判断上传文件是否在指定文件类型中
	if hz not in arr:
		return False
	fileurls = './static/pics/'+filename+'.'+hz
	# 用二进制的方式打开文件
	file = open(fileurls,'wb+')
	# 将文件分片写入
	for i in mypic.chunks():
		file.write(i)
	# 关闭文件
	file.close()
	# 返回制作完成的文件路径
	return '/static/pics/'+filename+'.'+hz