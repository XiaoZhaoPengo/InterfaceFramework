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


case_id = ['buy_product_order_review_01', 'buy_product_order_review_02', 'buy_product_order_review_03', 'buy_product_order_review_04', 'buy_product_order_review_05', 'buy_product_order_review_06', 'buy_product_order_review_07', 'buy_product_order_review_08', 'buy_product_order_review_09', 'buy_product_order_review_10', 'buy_product_order_review_11', 'buy_product_order_review_12', 'buy_product_order_review_13']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))


@allure.epic("开发平台接口")
@allure.feature("商品订单审核模块")
class TestBuyProductOrderReview:

    @allure.story("测试长租商品下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_buy_product_order_review(self, in_data, case_skip):
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
    pytest.main(['test_test_buy_product_order_review.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
