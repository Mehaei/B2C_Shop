from django import template
register = template.Library()


# 自定义标签
from django.utils.html import format_html
@register.simple_tag
def showpage(count,request):
    # count 总页码数 20
    # request 当前页面的请求对象
    # begin 开始页
    # eng 结束页

    # 获取所有参数,在每一次页码跳转时,携带已有的参数
    # <QueryDict: {'type': ['all'], 'keywords': ['41'], 'p': ['2']}>
    # ?keywords=41&type=all
    kv = '' 
    for x in request.GET:
        if x != 'p':
            kv+= '&'+x+'='+request.GET[x]

    count = int(count)
    # 在请求中获取当前页码数,如果没有 默认为1
    p = int(request.GET.get('p',1))

    begin = p - 4
    end = p + 5

    # 判断 如果当前页码数 小于5 
    if p < 5:
        begin = 1
        end = 10
    # 判断 如果当前页码数 大于 总页数-5
    if p > count-5:
        begin = count-9
        end = count

    # 判断如果 总页数 小于10
    if count < 10:
        begin = 1
        end = count

    page = ''
    page += '<li><a href="?p=1'+kv+'">首页</a></li>'
    # 上一页 当前页-1
    if p <= 1:
        page += '<li><a href="?p=1'+kv+'">上一页</a></li>'
    else:
        page += '<li><a href="?p='+str(p-1)+kv+'">上一页</a></li>'

    for x in range(begin,end+1):
        # 判断是否为当前页
        if x == p:
            page += '<li class="am-active"><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'
        else:
            page += '<li><a href="?p='+str(x)+kv+'">'+str(x)+'</a></li>'

    if p >= count:
        page += '<li><a href="?p='+str(count)+kv+'">下一页</a></li>'
    else:
        page += '<li><a href="?p='+str(p+1)+kv+'">下一页</a></li>'
        
    page += '<li><a href="?p='+str(count)+kv+'">尾页</a></li>'
   
    return format_html(page)


# 自定义标签
from django.utils.html import format_html
@register.simple_tag
def ascc(request):
    ktv = '' 
    for x in request.GET:
        if x != 'orr':
            ktv+= '&'+x+'='+request.GET[x]

    pagg = ''
    pagg += "<a href='?orr=up"+ktv+"'><span class='am-icon-caret-up'></span></a>"
    pagg += "<a href='?orr=down"+ktv+"'><span class='am-icon-caret-down'></span></a>"

    return format_html(pagg)

from django.utils.html import format_html
@register.simple_tag
def ride(price,num):
    
    price = float(price)

    num = int(num)

    total = price*num
    
    return '%.2f'%total