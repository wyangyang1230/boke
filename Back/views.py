from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from Back.models import *
import hashlib
from django.core.paginator import Paginator

# Create your views here.

# 登录装饰器
def LoginVaild(func):
    ## 1. 获取cookie中username和email
    ## 2. 判断username和email
    ## 3. 如果成功  跳转
    ## 4. 如果失败   login.html
    def inner(request,*args,**kwargs):
        email = request.COOKIES.get('email')
        userid = request.COOKIES.get('userid')
        ## 获取session
        session_email = request.session.get("email")
        if email and session_email and email == session_email:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Back/login/')
    return inner

# 密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# 注册
def register(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if email:
            ## 判断邮箱是否存在
            user = LoginUser.objects.filter(email=email).first()
            if not user:
                if password==password2:
                    user = LoginUser()
                    user.email = email
                    user.name = email
                    user.password = setPassword(password)
                    user.save()
                else:
                    error_msg = "两次密码不一致,请从新输入"
            else:
                error_msg = "邮箱已经被注册，请登录"
        else:
            error_msg = "邮箱不可以为空"

    return render(request,"Back/register.html",locals())

# 登录
def login(request):
    if request.method == "POST":
        error_msg = ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if LoginUser:
                ## 存在
                if user.password == setPassword(password):
                    ## 登录成功
                    ## 跳转页面
                    # error_msg = "登录成功"
                    # return HttpResponseRedirect('/index/')
                    ## 设置cookie
                    response  = HttpResponseRedirect("/Back/index/")
                    response.set_cookie("email",user.email)
                    response.set_cookie("userid",user.id)
                    request.session['email'] = user.email  ## 设置session
                    return response
                else:
                    error_msg = "密码错误"
            else:
                error_msg = "用户不存在"
        else:
            error_msg = "邮箱不可以为空"
    return render(request,"Back/login.html",locals())

# 首页
@LoginVaild
def index(request):
    return render(request,"Back/index.html")

# 登出
def logout(request):
    # 删除cookie   删除  session
    response = HttpResponseRedirect("/Back/login/")
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)

    return response

# 个人中心
def personal_info(request):
    user_id = request.COOKIES.get('userid')
    print(user_id)
    user = LoginUser.objects.filter(id=user_id).first()
    if request.method == "POST":
        data = request.POST
        print(data.get('email'))
        user.username = data.get('username')
        user.phone_number = data.get('phone_number')
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        user.photo = request.FILES.get("photo")
        user.save()
        print(data)
    return render(request,'back/personal_info.html',locals())

# 商品列表分页
# def goods_list(request,status,page=1):
#     page=int(page)
#     if status=="0":
#         #下架商品
#         goods_obj = Goods.objects.filter(goods_status=0).order_by('goods_number')
#     else:
#         #在售商品
#         goods_obj = Goods.objects.filter(goods_status=1).order_by('goods_number')
#     paginator=Paginator(goods_obj,10) #每页显示十条数据
#     page_obj=paginator.page(page)
#     nowpage=page_obj.number
#     start=nowpage-2
#     end=nowpage+2
#     page_range=paginator.page_range[start:end]
#     # print(page)
#     return render(request,'back/goods_list.html',locals())

# 文章详情
def get_article(request,id):
    id=int(id)
    article=Article.objects.get(id=id)
    return render(request,'back/get_article.html',locals())

# 增加文章
@LoginVaild
def add_article(request):
    article_type=Type.objects.all()
    author=Author.objects.all()
    print(author)
    if request.method=='POST':
        data=request.POST
        article=Article()
        article.title=data.get('title')
        article.description=data.get('description')
        article.content = data.get('content')
        article.picture=data.get('picture')
        article.save()

        article_type=request.POST.get('type') #获取文章类型id
        article.type=Type.objects.get(id=article_type)

        author_author = request.POST.get('author')
        article.author =Author.objects.get(id=author_author)

        user_id=request.COOKIES.get('userid')
        article.user=LoginUser.objects.get(id=user_id)
        article.save()
    return render(request, 'back/add_article.html', locals())


# 文章列表
@LoginVaild
def list_article(request,page=1):
    user_id=request.COOKIES.get('userid')
    page=int(page)
    article_obj=Article.objects.order_by('-date')
    paginator=Paginator(article_obj,5)
    page_obj=paginator.page(page)
    newpage=page_obj.number
    start=newpage-2
    end=newpage+2
    page_renge=paginator.page_range[start:end]
    return render(request,'back/list_article.html',locals())