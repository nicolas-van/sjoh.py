
from __future__ import unicode_literals, print_function, absolute_import

import unittest
import time
import datetime

import sjoh as json_serializer

class JsonSerializerTest(unittest.TestCase):

    def setUp(self):
        self.serializer = json_serializer.JsonSerializer()

    def test_timestamp(self):
        t = time.time()
        d = datetime.datetime.fromtimestamp(t)
        t2 = json_serializer._datetime_to_timestamp(d)
        self.assertTrue(abs(t - t2) < 0.001)

    def test_datetime(self):
        dth = json_serializer.DateTimeHandler()
        date = datetime.datetime.now()
        date = date.replace(microsecond=5000)
        jsoned = dth.to_json(date, None)
        self.assertTrue(isinstance(jsoned, dict))
        self.assertTrue(isinstance(jsoned["timestamp"], (int, long)))
        date2 = dth.from_json(jsoned, None)
        self.assertEqual(date, date2)

    def test_date(self):
        dh = json_serializer.DateHandler()
        date = datetime.date.today()
        jsoned = dh.to_json(date, None)
        self.assertTrue(isinstance(jsoned, dict))
        self.assertEqual(jsoned["year"], date.year)
        self.assertEqual(jsoned["month"], date.month)
        self.assertEqual(jsoned["day"], date.day)
        date2 = dh.from_json(jsoned, None)
        self.assertEqual(date, date2)

    def test_normal_json(self):
        test = {
            "firstName": "John",
            "lastName": "Smith",
            "isAlive": True,
            "age": 25,
            "height_cm": 167.64,
            "null": None,
            "false": False,
            "address": {
                "streetAddress": "21 2nd Street",
                "city": "New York",
                "state": "NY",
                "postalCode": "10021-3100"
            },
            "phoneNumbers": [
                { "type": "home", "number": "212 555-1234" },
                { "type": "fax",  "number": "646 555-4567" }
            ]
        }
        text = self.serializer.stringify(test)
        back = self.serializer.parse(text)
        text2 = self.serializer.stringify(back)
        self.assertEqual(text, text2)

    def test_json_datetime(self):
        date = datetime.datetime(1984, 11, 8, 12, 0, 0, 5000)
        text = self.serializer.stringify({"test": date})
        val = self.serializer.parse(text)
        self.assertEqual(val["test"], date)

    def test_json_date(self):
        date = datetime.date(1984, 11, 8)
        text = self.serializer.stringify({"test": date})
        val = self.serializer.parse(text)
        self.assertEqual(val["test"], date)

    def test_json_exception(self):
        ex = TestException("test")
        text = self.serializer.stringify(ex)
        conv_ex = self.serializer.parse(text)
        self.assertEqual(conv_ex.message, ex.message)
        self.assertEqual(conv_ex.type, json_serializer._fqn(type(ex)))
        self.assertEqual(conv_ex.traceback, None)
        text = self.serializer.stringify(conv_ex)
        conv_ex2 = self.serializer.parse(text)
        self.assertEqual(conv_ex2.message, conv_ex.message)
        self.assertEqual(conv_ex2.type, conv_ex.type)
        self.assertEqual(conv_ex2.traceback, conv_ex.traceback)

class TestException(Exception):
    pass