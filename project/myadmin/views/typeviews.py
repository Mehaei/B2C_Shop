from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types
from django.db.models import Q	
from django.contrib.auth.decorators import permission_required

@permission_required('myadmin.insert_types',raise_exception = True)

# 添加页
def typesadd(request):
	

	context = {'info':GetTypesAll()}

	return render(request,'admin/types/add.html',context)
	# return HttpResponse('商品列表页')

@permission_required('myadmin.insert_types',raise_exception = True)

# 执行添加
def typesinsert(request):
	try:
		db = Types()

		db.name = request.POST['name']
		db.pid = request.POST['pid']

		if db.pid == '0':
			db.path = '0/'
		else:
			a = Types.objects.get(id = db.pid)

			db.path = a.path+str(db.pid)+'/'
		db.save()
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('admin_types_list')+'"</script>')
	except:
		return HttpResponse('<script>alert("添加失败");location.href="'+reverse('admin_types_add')+'"</script>')

@permission_required('myadmin.show_types',raise_exception = True)

# 列表页
def typeslist(request):
	# 排序
	db = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
	abc(db)
	
	types = request.GET.get('types',None)
	# print(types)
	keywords = request.GET.get('keywords','')
	# print(type(keywords))
	re = Types.objects.all()

	arr = {'顶级分类':0}
	for i in re:
		arr[i.name] = i.pid
		# print(i.name)
		# print(i.pid)
	# print(arr)
	# ob = Types.objects.get(pid=arr.get(keywords))

	# print(keywords)
	if types:
		if types == 'all':			
			db = Types.objects.filter(Q(path__contains=arr.get(keywords,'aa'))|Q(name__contains=keywords)|Q(pid__contains=keywords)|Q(path__contains=keywords)|Q(id__contains=keywords))
			db = abc(db)
			print( 'types == all')

		elif types == 'name':
			db = Types.objects.filter(name__contains=keywords)
			db = abc(db)
			# print(db)
			# print( 'types ==name')


			# print(db)
	else:
		db = GetTypesAll()

	# 数据分页
	from django.core.paginator import Paginator

	# 实例化分页类
	paginator = Paginator(db,10)

	# 当前页码
	p = request.GET.get('p',1)
	# p = 1
	#根据当前页码获取当前页码显示的数据
	db = paginator.page(p) 
	# print(p)

	context = {'tlist':db}

	return render(request,'admin/types/list.html',context)
	# return HttpResponse('跳转成功，执行下一步')

# 将所属分类转为文字
def abc(db):
	# db = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
	for x in db:
		n = str(x.path).count('/')-1
		# print(n)
		x.name = (n * '|----')+x.name
		if x.pid == 0:

			x.pname = '顶级分类'
			x.path = '顶级分类'

		else:
			obj = Types.objects.get(id = x.pid)
			x.pname = obj.name
			x.path = '顶级分类'+'/'+obj.name +'/'

	return db

@permission_required('myadmin.edit_types',raise_exception = True)

# 修改页
def typesedit(request,tid):
	db = Types.objects.get(id = tid)

	# print(db.pid)
	context = {'info':db,'tlist':GetTypesAll()}
	return render(request,'admin/types/edit.html',context)
	# return HttpResponse('跳转成功，可执行下一步')

@permission_required('myadmin.edit_types',raise_exception = True)

# 执行修改
def typesupdate(request):
	try:
		db = Types.objects.get(id = request.POST['tid'])
		# print(db)

		db.name = request.POST['name']

		db.save()

		return HttpResponse('<script>alert("修改成功");location.href="'+reverse('admin_types_list')+'"</script>')
	except:

		return HttpResponse('<script>alert("修改失败");location.href="admin/types/edit/'+request.POST['tid']+'"</script>')

@permission_required('myadmin.del_types',raise_exception = True)
# 执行删除
def typesdel(request):

	ob = Types.objects.filter(pid = request.GET['tid']).count()
	# print(db)
	if ob:

		return JsonResponse({'status':1,'tx':'删除失败，当前类下含有子类'})

	db = Types.objects.get(id = request.GET['tid'])
	db.delete()
	# return HttpResponse(db)
	return JsonResponse({'status':0,'tx':'删除成功'})

# 查找类
def GetTypesAll():
	# select *,concat(path,id) as paths from myadmin_types order by paths;
	# db = Types.objects.all()
	db = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
	# db.query.group_by = ['pid']
	for x in db:
		n = str(x.path).count('/')-1
		# print(n)
		x.name = (n * '|----')+x.name
		# print(x.pid)
		if x.pid == 0:

			x.pname = '顶级分类'
			x.path = '顶级分类'
		else:
			obj = Types.objects.get(id = x.pid)
			x.pname = obj.name
			x.path = '顶级分类'+'/'+obj.name +'/'

	return db
