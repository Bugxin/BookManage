#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django import forms

from django.forms import widgets
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserForm(forms.Form):

    name = forms.CharField(min_length=6, max_length=12, label="用户名",
                           error_messages={"required": "该字段不能为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))

    pwd = forms.CharField(min_length=6, max_length=12, label="密码",
                          error_messages={"required": "该字段不能为空"},
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))

    r_pwd = forms.CharField(min_length=6, max_length=12, label="确认密码",
                            error_messages={"required": "该字段不能为空"},
                            widget=widgets.PasswordInput(attrs={"class": "form-control"}))

    email = forms.EmailField(label="邮箱",
                             error_messages={"required": "该字段不能为空", "invalid": "格式错误"},
                             widget=widgets.TextInput(attrs={"class": "form-control"}))

    tel = forms.CharField(min_length=11, max_length=11, label="手机号",
                          widget=widgets.TextInput(attrs={"class": "form-control"}))

    # 局部钩子 校验用户名
    def clean_name(self):
        val = self.cleaned_data.get("name")
        if not val.isdigit():
            user = User.objects.filter(username=val).first()
            if user:
                raise ValidationError("%s已注册" % user)
            return val
        else:
            raise ValidationError("用户名不能是纯数字!")

    # 全局钩子  校验 两次输入密码是否一致
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        r_pwd = self.cleaned_data.get('r_pwd')

        if pwd and r_pwd:  # 通过了局部钩子的校验才走 全局校验
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=32)
    age = forms.IntegerField()
    birth = forms.DateField()
    addr = forms.CharField(max_length=64)
    tel = forms.CharField(max_length=20)


class PulishForm(forms.Form):
    name = forms.CharField(max_length=32)
    city = forms.CharField(max_length=32)
    email = forms.EmailField()