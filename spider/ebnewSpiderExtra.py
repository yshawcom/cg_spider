# -*- coding: utf-8 -*-


"""
必联网
"""

__author__ = 'shaw'

import re

import execjs

from util import commonUtil


def cookie_jar_from_521(html):
    """
    处理响应码为521时的情况
    https://zhuanlan.zhihu.com/p/64750810
    """

    # 从html中提取出js
    js = ''.join(re.findall(r'<script language="javascript">(.*?)</script>', html))
    # 把最后自动执行的js字符串返回
    js = js.replace(r'eval("qo=eval;qo(po);");', 'return po;')

    # 找到方法名和参数
    name_and_arg = ''.join(re.findall(r'window\.onload=setTimeout\("([\s\S]*?)", \d+\);', js))
    func_name = name_and_arg[:name_and_arg.index('(')]
    func_arg = name_and_arg[name_and_arg.index('(') + 1:name_and_arg.index(')')]

    # 移除 window.onload=setTimeout("func(arg)", 200);
    func = re.sub(r'window\.onload=setTimeout\("([\s\S]*?)", \d+\);', '', js)

    # 执行js，获取执行结果
    context = execjs.compile(func)
    # document.cookie='https_ydclearance=1ad119645b8ed82f14ab775b-308d-4fb0-81f2-5620e9350455-1677578474; expires=Tue, 28-Feb-23 10:01:14 GMT; domain=.ebnew.com; path=/; Secure';window.document.location='/tradingSearch/index.htm'
    result = context.call(func_name, int(func_arg))

    # 从结果中提取cookie
    cookie_str = ''.join(re.findall(r"document\.cookie='(.*?)'", result))
    return commonUtil.cookie_str_2_jar(cookie_str)
