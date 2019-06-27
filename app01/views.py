from django.shortcuts import render,HttpResponse,reverse,redirect

# Create your views here.

from django.contrib import auth
from django.contrib.auth.models import User

from app01 import my_forms
from app01.models import *
from app01.my_pages import myPaginator
import json

# 首页
def index(request):
    login_state = request.session.get('is_login')
    username = request.session.get("username")
    return render(request, 'app01/index.html', locals())


# 查看书籍
def books(request):
    book_list = Book.objects.all()

    # 分页逻辑
    current_page = request.GET.get('page', 1)
    current_page = int(current_page)  # 当前页
    book_list, current_page, page_range = myPaginator(book_list, current_page)

    return render(request, 'app01/books.html', locals())


# 添加书籍
def addBook(request):
    if request.method == 'POST':
        data = json.loads(request.body, encoding='utf-8')
        title = data.get('title')
        price = data.get('price')
        date = data.get('date')
        publishid = data.get('publish_id')
        print('++++', data, title, price, date, publishid)
        res = {'state': False, 'msg': None}
        try:
            book_obj = Book.objects.create(title=title, price=price, publishDate=date, publish_id=publishid)
            book_obj.authors.set(data.get('authors_id_list'))
        except:
            res['msg'] = '添加失败'
        else:
            res['state'] = True
        finally:
            print('添加信息:=========>', res['msg'])
            return HttpResponse(json.dumps(res))


# 编辑书籍
def editBook(request, id):
    book_obj = Book.objects.filter(nid=id)[0]
    if request.method == 'POST':
        print('aaaa', request.body)
        data = json.loads(request.body, encoding='utf-8')
        print('bbbbb', data)
        price = data.get('price')
        date = data.get('date')
        publish = data.get('publish_id')
        author_id_list = data.get('authors_id_list')

        res = {'state': False, 'msg': None}

        # 更新书籍信息
        try:
            Book.objects.filter(nid=id).update(price=price, publishDate=date, publish_id=publish)
            book_obj.authors.set(author_id_list)
        except:
            res['msg'] = '检查更新字段是否合法'
        else:
            res['state'] = True
        finally:
            print('msg+++++', res['msg'])
            return HttpResponse(json.dumps(res))

    book_info = dict()
    book_info['id'] = book_obj.nid
    book_info['title'] = book_obj.title
    book_info['price'] = float(book_obj.price)
    book_info['publish'] = book_obj.publish.name
    book_info['author'] = []
    for item in book_obj.authors.all():
        book_info['author'].append(item.name)

    book_info['publish_date'] = book_obj.publishDate.strftime('%Y-%m-%d')

    # 设置ensure_ascii是为了能显示中文
    return HttpResponse(json.dumps(book_info, ensure_ascii=False))


# 删除书籍
def delBook(request, id):
    Book.objects.filter(nid=id).delete()

    return redirect('/app01/books')


# 获取所有的作者  ajax请求用
def get_authors(request):
    all_author = Author.objects.all()
    author_list = []
    for item in all_author:
        dic = dict()
        dic['id'] = item.nid
        dic['name'] = item.name
        author_list.append(dic)

    return HttpResponse(json.dumps(author_list, ensure_ascii=False))


# 作者列表 跳页面用
def authors(request):
    author_list = Author.objects.all()

    # 分页逻辑
    current_page = request.GET.get('page', 1)
    current_page = int(current_page)  # 当前页
    author_list, current_page, page_range = myPaginator(author_list, current_page)

    for item in AuthorDetail.objects.all():
        print(item, item.telephone, item.birthday)
    return render(request, 'app01/authors.html', locals())


# 作者代表作
def author_books(request, author_id):
    book_list = Book.objects.filter(authors__nid=author_id)

    # 分页逻辑
    current_page = request.GET.get('page', 1)
    current_page = int(current_page)  # 当前页
    book_list, current_page, page_range = myPaginator(book_list, current_page)
    return render(request, 'app01/author_books.html', locals())


# 获取所有的出版社  ajax请求用
def get_publishes(request):
    all_publish = Publish.objects.all()
    publish_list = []
    for item in all_publish:
        dic = dict()
        dic['id'] = item.nid
        dic['name'] = item.name
        publish_list.append(dic)
    return HttpResponse(json.dumps(publish_list, ensure_ascii=False))


# 出版社列表  跳页面用
def publishes(request):
    print('=======>', 1111)
    publish_list = Publish.objects.all()
    print('=======>', publish_list)
    # 分页逻辑
    current_page = request.GET.get('page', 1)
    current_page = int(current_page)  # 当前页
    publish_list, current_page, page_range = myPaginator(publish_list, current_page)
    return render(request, 'app01/publishes.html', locals())


# 出版社作品
def publish_books(request, publish_id):
    book_list = Book.objects.filter(publish_id=publish_id)

    # 分页逻辑
    current_page = request.GET.get('page', 1)
    current_page = int(current_page)  # 当前页
    book_list, current_page, page_range = myPaginator(book_list, current_page)
    return render(request, 'app01/publish_books.html', locals())


# 添加作者
def addauthor(request):
    if request.method == 'POST':
        data = json.loads(request.body, encoding='utf-8')
        form = my_forms.AuthorForm(data)
        print('author info:', data, type(data.get('birth')))
        res = {'state': False, 'msg': None}
        # 校验作者信息
        if form.is_valid():
            name = data.get('name')
            age = data.get('age')
            birth = data.get('birth')
            tel = data.get('tel')
            addr = data.get('addr')

            try:
                detail_obj = AuthorDetail.objects.create(birthday=birth, telephone=tel, addr=addr)
                Author.objects.create(name=name, age=age, authorDetail=detail_obj)
            except:
                res['msg'] = '添加失败'
            else:
                res['state'] = True
            finally:
                return HttpResponse(json.dumps(res, ensure_ascii=False))
        else:
            res['msg'] = '添加失败, 检查字段是否合法'
            print('form error: ', form.errors)
            return HttpResponse(json.dumps(res, ensure_ascii=False))


# 添加出版社
def addpublish(request):
    if request.method == 'POST':
        data = json.loads(request.body, encoding='utf-8')
        form = my_forms.PulishForm(data)
        print('publish info:', data)
        res = {'state': False, 'msg': None}

        # 校验 出版社信息 是否合法
        if form.is_valid():
            name = data.get('name')
            city = data.get('city')
            email = data.get('email')

            try:
                Publish.objects.create(name=name, city=city, email=email)
            except:
                res['msg'] = '添加失败'
            else:
                res['state'] = True
            finally:
                return HttpResponse(json.dumps(res, ensure_ascii=False))
        else:
            res['msg'] = '添加失败，检查字段合法性'
            print('add publish error', form.errors)
            return HttpResponse(json.dumps(res, ensure_ascii=False))


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        # 用户认证组件 验证用户名密码
        user = auth.authenticate(username=username, password=pwd)
        print(username, pwd, user)
        if user:
            request.session["is_login"] = True
            request.session["username"] = username
            auth.login(request, user)
            next_url = request.GET.get("next", "/app01/index/")
            return redirect(next_url)
        else:
            error = '用户名或密码不正确'
            return render(request, 'app01/login.html', {'error': error})
    return render(request, 'app01/login.html')


# 注册
def reg(request):
    if request.method == "POST":
        print('+++++++', request.POST)
        # 利用forms组件校验字段
        form = my_forms.UserForm(request.POST)

        if form.is_valid():
            #  校验成功 代表用户 未注册
            name = request.POST.get('name')
            pwd = request.POST.get('pwd')
            email = request.POST.get('email')

            # 注册用户
            user = User.objects.create_user(username=name, password=pwd, email=email)
            request.session["is_login"] = True
            request.session["username"] = name
            # 跳转回注册前的界面
            next_url = request.GET.get("next", "/app01/index/")
            return redirect(next_url)

        else:
            # 校验失败 提示出错信息
            errors = form.errors.get("__all__")
            print('错误信息:', errors)
            return render(request, "app01/reg.html", locals())

    form = my_forms.UserForm()

    return render(request, "app01/reg.html", locals())


# 注销
def logout(request):
    print('---->注销')
    auth.logout(request)
    return render(request, "app01/index.html")
