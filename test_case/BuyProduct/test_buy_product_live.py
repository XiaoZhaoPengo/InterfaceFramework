#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2024-07-29 11:39:40


import allure
import pytest
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.assertion.assert_control import Assert
from utils.requests_tool.request_control import RequestControl
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.teardown_control import TearDownHandler


case_id = ['buy_product_live_01', 'buy_product_live_02', 'buy_product_live_03', 'buy_product_live_04', 'buy_product_live_05', 'buy_product_live_06']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("开发平台接口")
@allure.feature("直播商品下单模块")
class TestBuyProductLive:

    @allure.story("直播测试商品下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_buy_product_live(self, in_data, case_skip):
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
    pytest.main(['test_test_buy_product_live.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
