# coding:utf8
import math
import io
import os
import uuid  # 生成32个随机的16进制数,防止用户上传图片重名
import random
from django.http import JsonResponse  # 返回一个json数据的相应
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
#from models import Class, Student, UserProfile, Text
from django.db.models import Q  # 模糊查找条件放入类中可以求并集
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger  # 一个分页处理类和3个异常
from django.contrib import auth  # 登陆,退出, 验证:login, logout, authenticate
from django.contrib.auth.decorators import login_required  # 登陆后方可访问的装饰器
from django.core.urlresolvers import reverse  # 重定向,反向解析
from django.contrib.auth.models import User  # 导入用户类:Django后台用户
from django.contrib.auth.hashers import make_password  # 使密码加密存储到数据库中
from django.db.models import Min, Max, Avg  # 数据库查询的聚合操作
from PIL import Image, ImageDraw, ImageFont  # 引入图片处理模块,用于生成验证码

from stumanage.models import Student

pageCount = 6  # 每个页面显示几条数据
stu_num = Student.objects.all()
# 总数除以每页显示几条,再向上取整,得到的是一共需要几页才能吧所有数据显示出来
max_page = int(math.ceil(float(len(stu_num))/float(pageCount)))
stu_num = range(1, max_page + 1)

# 提取学生信息的函数
def showStuInfo(pn):
    global pageCount
    stus = Student.objects.all()
    stus = pagination(stus, pageCount, pn)  # 调用分页函数
    context = {
        'stus': stus,
        'stu_num': stu_num
    }
    return context

# 分页函数
def pagination(qureySet, pageCount, pn):
    # 分页
    try:
        paginator = Paginator(qureySet, pageCount)  # 创建一个分页实例:参数1:Queryset结果集.参数2:每页显示条数
        qureySet = paginator.page(pn)  # 获取某页的信息
    except (InvalidPage, EmptyPage, PageNotAnInteger) as e:
        pn = 1
        qureySet = paginator.page(pn)  # 防止SB用户在输入框乱输入
        print(e)
    return qureySet

# 模糊检索函数
def icontains(sval):
    condition = Q(name__icontains=sval) | \
                Q(age__icontains=sval) | \
                Q(score__icontains=sval) | \
                Q(email__icontains=sval) | \
                Q(tel__icontains=sval) | \
                Q(className__name__icontains=sval)  # 牛逼的双下划线可以跨表
    stus = Student.objects.filter(condition)  # 模糊检索姓名
    return stus



# 主页面搜索引擎,不登陆也可以查询,只是不能进行管理相关的操作
def main(request):
    sval = request.GET.get('name')
    if sval is not None:
        stus = icontains(sval)  # 调用模糊检索函数
        return render(request, 'stumanage/main.html', {'stus': stus})
    return render(request, 'stumanage/main.html')

# 主页
@login_required
def index(request):
    return render(request, 'stumanage/index.html')

# 学生管理,展示学生信息
@login_required
def manage(request):
    global pageCount

    # 搜索框变量
    sval = request.GET.get('sval')
    pn = request.GET.get('pn',1)  # 去不到值就默认显示第一页

    # 获取排序图表中排序所需的参数,这两个参数需要随着点击被传到这里
    order = request.GET.get('order')  # 根据哪个字段来排序,页面中点击哪个字段,哪个字段就会被传过来
    rule = request.GET.get('rule')  # 排序规则,升序还是降序

    # 如果搜索框有东西就去查询,并返回查询到的内容,否则就显示全部信息
    if sval is not None:
        stus = icontains(sval)  # 调用模糊检索函数,返回一个Queryset

        # 将搜索出来的信息排序
        if order is not None:
            if rule == 'u':
                stus = stus.order_by(order)  # 升序
            else:
                stus = stus.order_by(order).reverse()  # 降序

        # 分页
        max_page = int(math.ceil(float(len(stus)) / float(pageCount)))  # 总数除以每页显示几条,再向上取整加1
        stu_num = range(1, max_page + 1)
        stus = pagination(stus, pageCount, pn)  # 调用分页函数

        context = {
            'stus': stus,
            'sval': sval,  # 这里将要查询的内容传到页面的作用是,在排序过程中,一直锁定包含这个关键字的信息
            'stu_num': stu_num
        }
        return render(request, 'stumanage/manage.html', context)  # 显示查询内容
    else:
        return render(request, 'stumanage/manage.html', showStuInfo(pn))  # 显示全部信息



# 增加学生信息
@login_required
def append(request):
    clss = Class.objects.all()
    context = {
        'clss': clss
    }
    return render(request, 'stumanage/append.html', context)

# 删除学生信息
@login_required
def deleteStuOfDB(request, id):
    Student.objects.get(pk=id).delete()  # 删除数据
    return HttpResponseRedirect(reverse('stumanage:manage',args=()))  # 如果不需要传参数时,args也已不用写

# 修改学生信息
@login_required
def changeStuOfDB(request, id):
    stu = Student.objects.get(pk=id)
    clss = Class.objects.all()
    context = {
        'stu': stu,
        'clss': clss
    }
    return render(request, 'stumanage/change.html', context)

# 上传图片函数 代码复用
def uploadFile(request, file):
    if file.content_type == 'image/jpeg' or file.content_type == 'image/gif':  # 判断文件格式
        if file.size / 1024 / 1024 < 2:  # 图片大小不能大于2M

            # 拼接文件路径,用于写文件时传给with:uuid生成32个16进制数
            uuidName = str(uuid.uuid4()) + "." + file.name.split(".")[-1]
            filePath = 'upload/avatar/' + uuidName  # ***
            absPath = os.path.dirname(filePath)  # 获取绝对路径
            if not os.path.exists(absPath):  # 判断路径是否存在,不存在则创建
                os.makedirs(absPath)

            with open(filePath, 'wb') as fileWrite:
                if file.multiple_chunks():  # 判断文件多个块是否为真, True代表文件大于2.5M,系统会拆解为多个块上传
                    for chunk in file.chunks():  # 遍历文件的所有块
                        fileWrite.write(chunk)  # chunk表示单块的内容,不需再读取
                else:
                    fileWrite.write(file.read())  # file.read()才表示整块的内容,不同的是需要先读取一下
            return True, uuidName
        else:
            return False, '图片大小不能超过2M'
    else:
        return False, '图片格式不正确'

# 存入数据库
@login_required
def saveStuToDB(request, id):
    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        score = request.POST.get('score')
        tel = request.POST.get('tel')
        avatar = request.FILES.get('avatar')
        className = request.POST.get('className')  # 数字1.2.3.4...

        uuidName = 'default.jpg'  # 当avatar为空时,也就是用户选择默认头像的时候给uuidName一个默认头像
        if avatar is not None:  # 如果用户上传了图片
            # 调用上传图片函数,上传成功返回True和图片名,上传失败返回False和相应的提示
            res = uploadFile(request, avatar)
            if res[0] is False:
                clss = Class.objects.all()  # 为避免用户选取无效的图片后页面刷新,不能显示班级信息
                return render(request, 'stumanage/append.html', {'avatarError': res[1], 'clss': clss})
            else:
                uuidName = res[1]

    stu = {
        'name': name,
        'age': age,
        'email': email,
        'score': score,
        'tel': tel,
        'className_id': int(className),
        'avatar': 'avatar/' + uuidName  # 这里必须将avatar一起存入数据库,与settings中的MEDIA_URL一起组成完整被访问路径
    }

    # 判断用户执行的添加信息还是修改信息
    if id != '0':
        Student.objects.filter(pk=id).update(**stu)  # 修改:更新数据
    else:
        Student.objects.create(**stu)  # 增加: 创建数据
    return HttpResponseRedirect(reverse('stumanage:manage'))

# 生成验证码
def createVerifycode(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(r'/usr/share/fonts/opentype/stix/STIXGeneral-BoldItalic.otf', 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # @@@@存入session，用于做进一步验证,用于和用户输入的做对比
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# 登陆
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        verifycode_client = request.POST.get('verifycode').upper()
        verifycode_sys = request.session.get('verifycode').upper()
        if username and password:  # 判断用户是否输入了用户名和密码
            user = auth.authenticate(username=username, password=password)  # 验证:通过返回一个数据对象,不通过返回一个None
            if user is not None:  # 判断是否通过验证
                if user.is_active:  # 判断账户是否时活跃状态,is_active是用户数据对象的一个属性
                    if verifycode_client == verifycode_sys:
                        # 登陆
                        auth.login(request, user)  # 参数:请求,用户对象
                        return HttpResponseRedirect('/stumanage/main/')
                    else:
                        return render(request, 'stumanage/login.html', {'error': '验证码错误'})
                else:
                    return render(request, 'stumanage/login.html', {'error': '用户被冻结'})
            else:
                return render(request, 'stumanage/login.html', {'error': '用户名或密码不正确'})
    else:
        return render(request, 'stumanage/login.html')

# 退出
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('stumanage:login'))

# 注册
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nick = request.POST.get('nick')
        phone = request.POST.get('phone')
        if username and password1 and password2:
            if password1 == password2:
                user_count = User.objects.filter(username=username).count()  # 过滤符合条件的数据数量,为0说明库里没有这个用户
                if user_count == 0:

                    # Django系统用户表
                    user_info = {
                        'username': username,
                        'password': make_password(password1)  # 将密码hash一下存入数据库,不然明文存储登陆不上
                    }
                    systemUser = User.objects.create(**user_info)  # 创建系统用户

                    # 用户拓展类
                    userProfile_info = {
                        'nick': nick,
                        'phone': phone,
                        'user': systemUser
                    }
                    UserProfile.objects.create(**userProfile_info)  # 创建拓展用户
                    return HttpResponseRedirect('/stumanage/index/')

                else:
                    return render(request, 'stumanage/register.html', {'error': '用户已存在'})
            else:
                return render(request, 'stumanage/register.html', {'error': '密码不一致'})
    return render(request, 'stumanage/register.html')

# 帮助文档
def helps(request):
    return render(request, 'stumanage/help.html')

# ajax加载测试页面
def ajaxPage(request):
    return render(request, 'stumanage/ajax-test.html')

# 相应ajax的请求,发送json数据
def ajaxLoadInfo(request):
    stus = Student.objects.all()
    stu_list = []
    for stu in stus:
        stu_list.append([stu.name, stu.age, stu.className_id])
    return JsonResponse({'data': stu_list})

# 富文本
def tinyMCE(request):
    return render(request, 'stumanage/tinymce.html')

# 保存富文本
def saveTinyMCE(request):
    if request.method == 'POST':
        blog = request.POST.get('text')
        content = {
            'text': blog
        }
        Text.objects.create(**content)
    return render(request, 'stumanage/tinymce.html')

# celery
from tasks import celeryTask
def celeryFunc(request):
    celeryTask.delay()  # 将耗时操作放到task中去执行
    return render(request, 'stumanage/celery.html')

# 测试页面
def testPage(request):
    stus = {}
    # stus = Student.objects.filter(pub_time__year=2017)
    stuAvg = Student.objects.aggregate(Avg('age'))
    stuMax = Student.objects.aggregate(Max('age'))
    stuMin = Student.objects.aggregate(Min('age'))
    stus['stuAvg'] = stuAvg
    stus['stuMax'] = stuMax
    stus['stuMin'] = stuMin
    return render(request, 'stumanage/testpage.html', stus)






