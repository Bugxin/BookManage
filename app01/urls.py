#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.urls import path, re_path

from app01 import views

urlpatterns = [
    path('index/', views.index, name='index'),   # 首页
    path('books/', views.books, name='books'),   # 书籍列表
    path('addBook/', views.addBook, name='addBook'),  # 添加书籍
    re_path('editBook/(\d+)/', views.editBook, name='editBook'),  # 编辑书籍
    re_path('delBook/(\d+)/', views.delBook, name='delBook'),  # 删除书籍
    path('publishes/', views.publishes, name='publishes'),   # 出版社列表
    re_path('publish_books/(\d+)/', views.publish_books, name='publish_books'),  # 出版社书籍列表
    path('authors/', views.authors, name='authors'),  # 作者列表
    re_path('author_books/(\d+)/', views.author_books, name='author_books'),  # 作品列表
    path('get_authors/', views.get_authors, name='get_authors'),  # 获取所有的作者
    path('get_publishes/', views.get_publishes, name='get_publishes'),  # 获取所有的出版社
    path('addpublish/', views.addpublish, name='addpublish'),  # 添加出版社
    path('addauthor/', views.addauthor, name='addauthor'),  # 添加作者
    path('login/', views.login, name='login'),   # 登录
    path('reg/', views.reg, name='reg'),   # 注册
    path('logout/', views.logout, name='logout'),   # 注销
    re_path('^$', views.index, name='index'),   # 默认界面
]
