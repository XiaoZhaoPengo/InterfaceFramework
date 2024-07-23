#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024-07-23 14:18:52


import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.requests_tool.request_control import RequestControl
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


case_id = ['buy_product_dev_long_01', 'buy_product_dev_long_02', 'buy_product_dev_long_03', 'buy_product_dev_long_04', 'buy_product_dev_long_05', 'buy_product_dev_long_06', 'buy_product_dev_long_07', 'buy_product_dev_long_08', 'buy_product_dev_long_09', 'buy_product_dev_long_10']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("开发平台接口")
@allure.feature("测试商品下单模块")
class TestBuyProductDevLong:

    @allure.story("测试长租商品下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_buy_product_dev_long(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()


if __name__ == '__main__':
    pytest.main(['test_test_buy_product_dev_long.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
