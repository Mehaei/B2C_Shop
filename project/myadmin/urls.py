"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . views import views,typeviews,goodsviews,orderviews,authviews

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 登录页面
    url(r'^$',authviews.adminlogin,name="admin_login"),
    # 登录验证
    # url(r'^logintest$',views.logintest,name="logintest"),
     # 验证码 verifycode
    url(r'^getvcode/$',views.verifycode,name='getvcode'),
    # 退出登录,清除session
    url(r'^loginout/$',authviews.adminloginout,name='admin_loginout'),
    

    # 后台管理员添加页面
    url(r'^admin/add$',views.admin_add,name = "admin_add"),
    # 执行管理员数据插入
    url(r'^admin/insert$',views.admin_insert,name = "admin_insert"),
    # 管理员列表页
    url(r'^admin/list$',views.admin_list,name = "admin_list"),
    # 修改管理员状态
    url(r'^admin/status$',views.admin_status,name = "admin_status"),
    # 执行管理员账户删除
    url(r'^admin/del/(?P<tid>[0-9]+)$',views.admin_del,name = "admin_del"),

    # 后台权限管理
    #后台管理员添加
    url(r'^auth/user/add$',authviews.useradd,name = "auth_user_add"),
    # 后台管理员用户列表
    url(r'^auth/user/list$',authviews.userlist,name = "auth_user_list"),
    # 后台管理员删除
    url(r'^auth/user/del(?P<uid>[0-9]+)$',authviews.userdel,name = "auth_user_del"),
    
    #权限组添加
    url(r'^auth/group/add$',authviews.groupadd,name = "auth_group_add"),
    # 权限组列表
    url(r'^auth/group/list$',authviews.grouplist,name = "auth_group_list"),
    #后台管理组删除
    url(r'^auth/group/edit/(?P<gid>[0-9]+)$',authviews.groupedit,name = "auth_group_edit"),


    # 首页数据显示
    url(r'^index/baseqeust/$',views.base_qeust,name="base_quest"),


    # 后台管理首页
    url(r'^index$',views.adminindex,name="admin_index"),
    # 添加会员页面
    url(r'^user/add/$',views.useradd,name="admin_user_add"),
    # 执行会员添加
    url(r'^user/adduser/$',views.userinsert,name="admin_user_insert"),

    # 用户列表页
    url(r'^user/list/$',views.userlist,name="admin_user_list"),
    # 用户修改页
    url(r'^user/edit/(?P<uid>[0-9]+)$',views.useredit,name="admin_user_edit"),

    # 执行修改
    url(r'^user/update/$',views.userupdate,name="admin_user_update"),
    # 执行删除
    url(r'^user/del/$',views.userdel,name="admin_user_del"),

    # 点击下拉框修改用户账户状态
    url(r'^user/status/$',views.userstatus,name="admin_user_status"),



# 商品分类管理
    # 商品分类添加页
    url(r'^types/add/$',typeviews.typesadd,name="admin_types_add"),
    # 执行添加
    url(r'^types/insert/$',typeviews.typesinsert,name="admin_types_insert"),
    # 列表页
    url(r'^types/list/$',typeviews.typeslist,name="admin_types_list"),
    # 修改页
    url(r'^types/edit/(?P<tid>[0-9]+)$',typeviews.typesedit,name="admin_types_edit"),
    # 执行修改页
    url(r'^types/update/$',typeviews.typesupdate,name="admin_types_update"),
    # 执行删除
    url(r'^types/del/$',typeviews.typesdel,name="admin_types_del"),



# 商品模块
    # 商品添加页面
    url(r'^goods/add/$',goodsviews.goodsadd,name="admin_goods_add"),
    # 执行商品添加
    url(r'^goods/insert/$',goodsviews.goodsinsert,name="admin_goods_insert"),
    # 商品列表页
    url(r'^goods/list/$',goodsviews.goodslist,name="admin_goods_list"),
    # 商品修改页
    url(r'^goods/edit/(?P<tid>[0-9]+)$',goodsviews.goodsedit,name="admin_goods_edit"),
    # 执行商品修改
    url(r'^goods/edit/$',goodsviews.goodsupdate,name="admin_goods_update"),
    # 修改商品状态
    url(r'^goods/status/$',goodsviews.goodsstatus,name="admin_goods_status"),
    # 执行商品删除
    url(r'^goods/del/$',goodsviews.goodsdel,name="admin_goods_del"),


# 订单管理
    # 订单列表
    url(r'^order/list/$',orderviews.orderlist,name="admin_order_list"),
    # 修改订单状态
    url(r'^order/status/$',orderviews.orderstatus,name="admin_order_status"),
    # 订单详情
    url(r'^order/info/(?P<oid>[0-9]+)$',orderviews.orderinfo,name="admin_order_info"),

]
