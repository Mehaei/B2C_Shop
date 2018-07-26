from django.db import models

# Create your models here.
# 会员管理
class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=80)
	email = models.CharField(max_length=100,null=True)
	phone = models.CharField(max_length=11,null=True)
	sex = models.CharField(max_length=1,null=True)
	age = models.IntegerField(null=True)
	picurl = models.CharField(max_length=100,default='/static/pics/default/default.jpg')
	# 0 正常　１禁用 3逻辑删除
	status = models.IntegerField(default=0)
	addtime = models.DateTimeField(auto_now_add=True)

	class Meta:
        # 制定权限
		permissions = (
				("show_users",'查看会员管理'),
                ("insert_users",'添加会员'),
                ("edit_users",'修改会员'),
                ("del_users",'删除会员'),
        )
# 登录后台管理员
class Admin(models.Model):
	adminname = models.CharField(max_length=50)
	password = models.CharField(max_length=80)
	# 0正常 1禁用
	status = models.IntegerField(default=0)
	addtime = models.DateTimeField(auto_now_add=True)

# 商品列表管理
class Types(models.Model):
	name = models.CharField(max_length=50)
	pid = models.IntegerField()
	path = models.CharField(max_length=50)

	class Meta:
        # 制定权限
		permissions = (
                ("show_types",'查看商品分类管理'),
                ("insert_types",'添加商品分类'),
                ("edit_types",'修改商品分类'),
                ("del_types",'删除商品分类'),
        )
# 商品模型
class Goods(models.Model):
    # 商品所属分类
    typeid = models.ForeignKey(to="Types", to_field="id")
    # 商品标题
    title = models.CharField(max_length=255)
    # 商品价格
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # 商品库存
    storage = models.IntegerField()
    # 商品图片
    pic = models.CharField(max_length=50)
    # 商品详情
    info = models.TextField()
    # 购买数量
    num  =  models.IntegerField(default=0)
    # 点击次数
    clicknum =  models.IntegerField(default=0)
    # 商品状态 1：新品、2：热销、3：下架
    status = models.IntegerField(default=1)
    # 商品添加时间
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 制定权限
        permissions = (
                ("show_goods",'查看商品管理'),
                ("insert_goods",'添加商品'),
                ("edit_goods",'修改商品'),
                ("del_goods",'删除商品'),
        )

class Address(models.Model):
    # 用户ＩＤ
    uid = models.ForeignKey(to="Users",to_field="id")
    # 收货人
    uname = models.CharField(max_length=50)
    # 收货地址
    uaddr = models.CharField(max_length=255)
    # 收货电话
    uphone = models.CharField(max_length=11)
    # 默认地址　　默认为０
    status = models.IntegerField(default = 1)

    class Meta:
        # 制定权限
        permissions = (
                ("show_address",'查看地址管理'),
                ("insert_address",'添加地址'),
                ("edit_address",'修改地址'),
                ("del_address",'删除地址'),
        )


class Order(models.Model):
    # 用户ｉｄ
    uid = models.ForeignKey('Users',to_field='id')
    # 收货地址详情
    address = models.ForeignKey('Address',to_field='id')
    #订单总价
    totalprice = models.FloatField()
    #订单总数数量
    totalnum = models.IntegerField()
    #1未付款　２．带发货　３．带收货　４.待评价　５．已取消
    # 订单状态
    stauts = models.IntegerField()
    # 订单创建时间
    addtime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # 制定权限
        permissions = (
                ("show_order",'查看订单管理'),
                ("insert_order",'添加订单'),
                ("edit_order",'修改订单'),
                ("del_order",'删除订单'),
        )


class OrderInfo(models.Model):
    # 订单号
    orderid = models.ForeignKey('Order',to_field='id')
    # 商品信息
    gid = models.ForeignKey('Goods',to_field='id')
    # 单个商品数量
    num = models.IntegerField()
    # 单个商品单价
    price = models.FloatField()
