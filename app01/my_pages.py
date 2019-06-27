#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def myPaginator(objects, current_page, per_page=4, max_show_pages=11):
    """
    :param objects:    要分页的对象列表
    :param current_page:   当前页
    :param per_page:       每页展示多少条
    :param max_show_pages:  最多展示多少页
    :return:
    """
    # 以当前页为中心 左右需要展示的页数
    mid_show_page = max_show_pages / 2

    paginator = Paginator(objects, per_page)
    if paginator.num_pages > max_show_pages:

        # 当前页为小于mid_show_page的数时 不会出现负数边界的判断
        if current_page - mid_show_page < 1:
            page_range = range(1, max_show_pages)

            # 当前页的范围不超过最大页数的边界判断
        elif current_page + mid_show_page > paginator.num_pages:
            page_range = range(current_page - mid_show_page, paginator.num_pages + 1)

        # 正常左5右5
        else:
            page_range = range(current_page - mid_show_page, current_page + mid_show_page)

    else:
        page_range = paginator.page_range

    try:
        objects = paginator.page(current_page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects, current_page, page_range


