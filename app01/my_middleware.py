#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import redirect
from BookManage import settings


class myLogin(MiddlewareMixin):
    def process_request(self, request):
        # 获取当前页面的路由
        path = request.path
        print('当前请求界面:', path)
        print('当前请求全路径:', request.get_full_path())

        login_state = request.session.get('is_login')
        print('登录状态：', login_state)
        # print('白名单：',  settings.PATH_WHITE_LIST)

        # 不在白名单的且未登录  都要验证登录
        if login_state is None:
            if path not in settings.PATH_WHITE_LIST:
                return redirect('/app01/login/?next=%s' % path)



