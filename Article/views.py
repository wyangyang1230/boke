from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from Back.models import *

# Create your views here.


 ## 父模板
def base(request):
    # get请求
    data=request.GET
    serach=data.get('serach')
    print(serach)
    # 通过form表单提交的数据，判断数据库中是否存在某个文章
    # 通过模型查询
    article=Article.objects.filter(title__contains=serach).all()
    print(article)
    return render(request,'article/base.html',locals())


# 网站首页
def index(request):
    article=Article.objects.order_by('-date')[:6]
    recommend_article=Article.objects.filter(recommend=1)[:7]
    click_article=Article.objects.order_by('-click')[:12]

    return render(request,'article/index.html',locals())


# 个人相册
def listpic(request):
    return render(request,'article/listpic.html')

# 个人简介
def about(request):
    return render(request,'article/about.html')

# 文章分页
def newslistpic(request,page=1):
    page=int(page) #1为字符串类型，需要将类型转换
    article=Article.objects.order_by('-date')
    paginator=Paginator(article,6)  #显示每页6条数据
    page_obj=paginator.page(page)
    # 获取当前页
    current_page=page_obj.number
    start=current_page-3
    if start<1:
        start=0
    end=current_page+2
    if end > paginator.num_pages:
        end = paginator.num_pages
    if start==0:
        end=5
    if end==paginator.num_pages:
        start=paginator.num_pages-5
    page_range=paginator.page_range[start:end]
    return render(request,'article/newslistpic.html',locals())


# 文章详情
def articledetails(request,id):
    # id为字符串类型
    id=int(id)
    article=Article.objects.get(id=id)
    print(article)
    return render(request,'article/articledetails.html',locals())