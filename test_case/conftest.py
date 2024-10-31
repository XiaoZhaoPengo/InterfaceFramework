#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/3/30 14:12
# @Author : 余少琪
import json

import pytest
import time
import allure
import requests
import ast
from common.setting import ensure_path_sep
from utils.requests_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tools.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    del_file(ensure_path_sep("\\report"))


def send_verification_code():
    """
        发送验证码请求
        :return:
    """
    url = "http://dev.adminapi.zuzuya.cn/v1.0/admin/getSmsCode?phone=18271421203"
    headers = {'Content-Type': 'application/json'}
    # 请求验证码接口
    res = requests.get(url=url, headers=headers, verify=True)
    response_res = res.json()
    print(response_res)
    return response_res


@pytest.fixture(scope="session", autouse=True)
def admin_login_init():
    """
    获取后台登录的cookie
    :return:
    """
    # 先发送验证码请求
    verification_response = send_verification_code()
    
    # 等待一段时间，确保验证码已被发送和处理
    time.sleep(1.5)  # 假设需要等待5秒，根据实际情况调整
    
    url = "http://dev.adminapi.zuzuya.cn/v1.0/admin/smsLogin"
    data = {
        "code": "1234",
        "device": "pc",
        "userName": "18271421203"
    }
    headers = {'Content-Type': 'application/json'}
    # 请求登录接口
    data = json.dumps(data)
    
    res = requests.post(url=url, data=data, verify=True, headers=headers)
    response_cookie = res.cookies
    
    response_token = res.json()
    print(response_token)
    cookies = ''
    for k, v in response_cookie.items():
        _cookie = k + "=" + v + ";"
        # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
        cookies += _cookie
        # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
    # CacheHandler.update_cache(cache_name='login_cookie', value=cookies)
    # 将登录接口中的token写入缓存中，其中login_token是缓存名称
    token = response_token['details']['token']
    print(token)
    CacheHandler.update_cache(cache_name='admin_token', value=token)

@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    获取app登录的cookie
    :return:
    """
    
    url = "https://dev.api.zuzuya.cn/minialiapp/user/phoneAuth"
    data = {
        "auth_code": '818887e9020b4c8a850cb37f4701TC77',
        "phoneData": "{\"response\":\"lHMEErMZCAjMYopf4Fl0RdSUmwvUQfIkf1lDslVJ9U9Bw9+GhlNPtShcFC6SkiWBpJE1rDnDeVjUAuaya5rpJg==\",\"sign\":\"RFISYSozx5AsTSpwcWdt/JtBhO2+3gtI+MNljC9+fyBDCOxMA5me13M372YY0uA6uUYufrBGUicFepxzb49ArUN511HbOSRw6NqYV23wxzDTJtT2/9uvgJn4HRu4R1YjVaU7jqVQ+m081g8XSW1tS4Ey8Ns0lY8Xwy35Rso7/lE7UuLULrbSsFYQBrojPGTwo09R7UiQTfVMxhEMZTrI5XtxNgir6dkVBZ+M+tnenqRf+OzpTbigfYTCs0x70YcKelIz7EYtBLK/fwGVVPd3Ub/d5UCJYG5raAutTr9E0Uw2VLRC41ChIGoSW7SZDxgcz2S3urPbFLqgWmPhAwDE3w==\"}",
        "clientType": 'alipayMiniapp'
    }
    
    headers = {'Content-Type': 'application/json', "from": '', 'appId': '2021001199645150',
               'fromAuthCode': '397f11cffed949048762fccfa3d4PA77'}
    # 请求登录接口
    data = json.dumps(data)
    res = requests.post(url=url, data=data, verify=True, headers=headers)
    # print(res.json())
    response_cookie = res.cookies
    print(response_cookie)
    response_token = res.json()
    # print(response_token)
    
    cookies = ''
    for k, v in response_cookie.items():
        _cookie = k + "=" + v + ";"
        # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
        cookies += _cookie
        # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
    # CacheHandler.update_cache(cache_name='login_cookie', value=cookies)
    
    # 将登录接口中的token写入缓存中，其中login_token是缓存名称
    user_token = response_token['details']['userToken']
    print(user_token)
    CacheHandler.update_cache(cache_name='login_token', value=user_token)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    # 期望用例顺序
    # print("收集到的测试用例:%s" % items)
    appoint_items = ["test_get_user_info", "test_collect_addtool", "test_Cart_List", "test_ADD", "test_Guest_ADD",
                     "test_Clear_Cart_Item"]

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


def pytest_configure(config):
    config.addinivalue_line("markers", 'smoke')
    config.addinivalue_line("markers", '回归测试')


@pytest.fixture(scope="function", autouse=True)
def case_skip(in_data):
    """处理跳过用例"""
    in_data = TestCase(**in_data)
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        allure.dynamic.title(in_data.detail)
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")

if __name__ == '__main__':
    admin_login_init()