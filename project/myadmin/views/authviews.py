from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,login,logout

# 管理员添加
def useradd(request):
	# 判断请求当时
	if request.method == 'GET':
		#查询所有组的信息
		glist = Group.objects.all()
		# print(glist)
		return render(request,'auth/user/add.html',{'glist':glist})
	elif request.method == 'POST':

		# 如果选中了超级管理员
		if request.POST['is_superuser'] == '1':

			ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
		
		else:
			ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
			
		ob.save()
		# 判断是否选中权限
		ds = request.POST.getlist('ds',None)

		if ds:
			# 将用户加入组中
			ob.groups.set(ds)

			ob.save()
	
		return HttpResponse('<script>location.href="'+reverse('auth_user_list')+'"</script>') 
		

# 管理员列表
def userlist(request):
	# 查询所有的管理员
	db = User.objects.all()

	return render(request,'auth/user/list.html',{'alist':db})
	# return HttpResponse('userlist')


# 用户组添加
def groupadd(request):
	if request.method == 'GET':
		# 查询除了django自定义的权限
		perms = Permission.objects.exclude(name__istartswith='Can')

		return render(request,'auth/group/add.html',{'perms':perms})
	# 当执行添加的时候
	elif request.method == 'POST':
		# 添加组
		ob = Group(name=request.POST['name'])

		ob.save()
		# 判断是否选中权限
		perms = request.POST.getlist('perms',None)

		if perms:
			# 将权限分配到组
			ob.permissions.set(perms)

			ob.save()


		return HttpResponse('<script>location.href="'+reverse('auth_group_list')+'"</script>') 

# 用户组列表
def grouplist(request):
	# 查询所有的组
	data = Group.objects.all()
	# print(data)
	return render(request,'auth/group/list.html',{'alist':data})

# 用户组的修改
def groupedit(request,gid):
	# 查询当前修改的组
	ginfo = Group.objects.get(id=gid)

	if request.method == 'GET':
		# 查询除了django自带的权限和已拥有的全选
		perms = Permission.objects.exclude(name__istartswith='Can').exclude(group=ginfo)


		return render(request,'auth/group/edit.html',{'ginfo':ginfo,'perms':perms})

	elif request.method == 'POST':
		#执行修改
		ginfo.name = request.POST['name']
		# 获取选中的权限
		perms = request.POST.getlist('perms',None)
		# 执行删除之前的所有权限
		ginfo.permissions.clear()

		if perms:
			# 写入新的权限
			ginfo.permissions.set(perms)

		ginfo.save()

		return HttpResponse('<script>location.href="'+reverse('auth_group_list')+'"</script>') 

# 登录页面
def adminlogin(request):
	# 如果是get请求
	if request.method == 'GET':
		# 返回登录页
		return render(request,'admin/login.html')
	# 如果是post请求 则验证登录
	elif request.method == 'POST':

		# 判断验证码是否正确
		if request.POST['vcode'].lower() != request.session['verifycode'].lower():
			# 如不正确返回登录页
			return HttpResponse('<script>alert("验证码不正确");location.href="'+reverse('admin_login')+'"</script>')
		  # 使用django提供的后台用户验证方法
		username = request.POST['adminname']

		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
            #登录
			login(request,user)
			# 验证成功 跳转首页
			return HttpResponse('<script>alert("大哥，欢迎回家");location.href="'+reverse('admin_index')+'"</script>')



	# 	# 获取登录账户的整条数据
	# 	db = Admin.objects.filter(adminname = request.POST['adminname'])
	# 	# print(db[0].password)
	# 	if db:
	# 		db = db[0]
	# 		# 判断密码是正确
	# 		if check_password(request.POST['password'],db.password):
	# 			if db.status == 0:
	# 				# 写入session
	# 				request.session['AdminUser'] = {'name':db.adminname}
					# # 验证成功 跳转首页
					# return HttpResponse('<script>alert("大哥，欢迎回家");location.href="'+reverse('admin_index')+'"</script>')
		
		return HttpResponse('<script>alert("账户不存在或密码不正确");location.href="'+reverse('admin_login')+'"</script>')

# 退出登录
def adminloginout(request):
	# del request.session['AdminUser']
	# 退出登录
	logout(request)
	return HttpResponse('<script>alert("退出成功");location.href="/admin"</script>')

# 管理员用户的删除
def userdel(request,uid):
	ob = User.objects.get(id = uid)

	ob.delete()

	return HttpResponse('<script>location.href="'+reverse('auth_user_list')+'"</script>') 

	



