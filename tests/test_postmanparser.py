import unittest
import os
import json
import shutil
from postman2case.core import PostmanParser
from postman2case.parser import parse_value_from_type


class TestParser(unittest.TestCase):

    def setUp(self):
        self.postman_parser = PostmanParser("tests/data/test.json")

    def test_init(self):
        self.assertEqual(self.postman_parser.postman_testcase_file, "tests/data/test.json")

    def test_read_postman_data(self):
        with open("tests/data/test.json", encoding='utf-8', mode='r') as f:
            content = json.load(f)
        other_content = self.postman_parser.read_postman_data()
        self.assertEqual(content, other_content)

    def test_parse_url(self):
        request_url = {
            "raw": "https://postman-echo.com/get?foo1=bar1&foo2=bar2",
            "protocol": "https",
            "host": [
                "postman-echo",
                "com"
            ],
            "path": [
                "get"
            ],
            "query": [
                {
                    "key": "foo1",
                    "value": "bar1"
                },
                {
                    "key": "foo2",
                    "value": "bar2"
                }
            ]
        }
        url = self.postman_parser.parse_url(request_url)
        self.assertEqual(url, request_url["raw"])

        request_url = "https://postman-echo.com/get?foo1=bar1&foo2=bar2"
        url = self.postman_parser.parse_url(request_url)
        self.assertEqual(url, request_url)

    def test_parse_header(self):
        request_header = [
            {
                "key": "Content-Type",
                "name": "Content-Type",
                "value": "application/json",
                "type": "text"
            }
        ]
        target_header = {
            "Content-Type": "application/json"
        }
        header = self.postman_parser.parse_header(request_header)
        self.assertEqual(header, target_header)

        header = self.postman_parser.parse_header([])
        self.assertEqual(header, {})

    def test_parse_each_item_get(self):
        with open("tests/data/test_get.json", encoding='utf-8', mode='r') as f:
            item = json.load(f)

        result = {
            "name": "test_get",
            "validate": [],
            "variables":
                {
                    "search": "345"
                },
            "request": {
                "method": "GET",
                "url": "http://www.baidu.com",
                "headers": {},
                "params": {
                    "search": "$search"
                }
            }
        }

        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)

    def test_parse_each_item_post(self):
        with open("tests/data/test_post.json", encoding='utf-8', mode='r') as f:
            item = json.load(f)

        result = {
            "name": "test_post",
            "validate": [],
            "variables":
                {
                    "q": "search",
                    "testerhome": None,
                    "method": "POST"
                }
            ,
            "request": {
                "method": "POST",
                "url": "https://postman-echo.com/post",
                "headers": {
                    "Content-Type": "application/json"
                },
                "json": {"method": "$method"},
                "params": {
                    "q": "$q",
                    "testerhome": "$testerhome"
                }
            }
        }
        fun_result = self.postman_parser.parse_each_item(item)
        self.assertEqual(result, fun_result)

    def test_parse_data(self):
        result = self.postman_parser.parse_data()
        self.assertEqual(len(result), 21)

    def test_save(self):
        result = self.postman_parser.parse_data()
        self.postman_parser.save(result, "save")
        shutil.rmtree("save")

    def test_parse_value_from_type(self):
        value_list = [(1, 1), ('2', '2'), ('true', True), ('false', False), (3.1, 3.1), (None, None)]
        for i in value_list:
            self.assertEqual(parse_value_from_type(i[0]), i[1])
