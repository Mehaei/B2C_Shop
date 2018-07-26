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
from django.contrib import admin
from . import views
urlpatterns = [
	# 首页
    url(r'^$', views.index,name='index'),
    url(r'^emailss/$', views.emailss,name='emailss'),
    #注册页
    url(r'^register/$', views.register,name='register'),
    # 登录页
    url(r'^login/$', views.login,name='login'),
    # 退出登录
    url(r'^loginout/$', views.loginout,name='loginout'),

    # 忘记密码
    url(r'^forget/$', views.forget,name='forget'),
    # 修改密码页
    url(r'^forgetedit/forgetnew/(?P<uid>[0-9]+)$', views.forgetnew,name='forgetnew'),
    # 填写忘记密码的邮箱
    url(r'^forgetedit/$', views.forget_edit,name='forget_edit'),
    # 执行密码的修改
    url(r'^forgetnew/insert$', views.forget_new_insert,name='forgetnew_insert'),


    # 列表页
    url(r'^list/(?P<tid>[0-9]+)$', views.list,name='list'),
    # 详情页
    url(r'^info/(?P<gid>[0-9]+)$', views.info,name='info'),
    # 添加购物车
    url(r'^cartadd/$', views.cartadd,name='cartadd'),
    # 购物车列表
    url(r'^cartlist/$', views.cartlist,name='cartlist'),
    # 清空购物车
    url(r'^cartclear/$', views.cartclear,name='cartclear'),
    # 删除商品
    url(r'^delone/(?P<gid>[0-9]+)$', views.delone,name='delone'),

    # 商品数量修改
    # 减少
    url(r'^subtract/$', views.subtract,name='subtract'),
    # 增加
    url(r'^subadd/$', views.subadd,name='subadd'),

    # 订单确认　　
    url(r'^order/confirm/$', views.order_confirm,name='order_confirm'),
    
    url(r'^order/confirmm/(?P<gid>[0-9]+)$', views.order_confirmm,name='order_confirmm'),
 
    # 创建订单
    url(r'^order/create/$', views.order_create,name='order_create'),
    #我的订单
    url(r'^myorder/$', views.myorder,name='myorder'),

    # 确认用户付款　修改用户状态
    url(r'^order/edit/status/$', views.edit_order_status,name='edit_order_status'),

    # 个人中心
    url(r'^mycenter/$', views.my_center,name='my_center'),
    # 地址管理
    url(r'^address/manage/$', views.address_manage,name='address_manage'),
    # 地址修改
    url(r'^address/edit/$', views.address_edit,name='address_edit'),
    # 地址删除
    url(r'^address/del/(?P<tid>[0-9]+)/$', views.address_del,name='address_del'),
    # 地址添加
    url(r'^address/add/$', views.address_add,name='address_add'),
    
    # 我的个人中心修改
    url(r'^mycenter/edit/$', views.mycenter_edit,name='mycenter_edit'),
    # 订单状态修改
    url(r'^order/status/edit/$', views.order_status_edit,name='order_status_edit'),
    # 删除 取消订单
    url(r'^order/del/$', views.order_del,name='order_del'),

    # 订单详情
    url(r'^order/info/(?P<uid>[0-9]+)/$', views.order_info,name='order_info'),
]
