# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 09:21:34 2021

@author: wsycx
"""
import requests
import json

BASE = "http://127.0.0.1:5000/"
try: 
    from ramp import app 
    import unittest
except Exception as e: 
    print("some modules are missing {} ".format(e))
    
class Flasktest(unittest.TestCase):
    def test_args_none(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : None})
        self.assertEqual(response.json()['message']['length_unit'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")

    def test_one_args(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : "mm"})
        self.assertEqual(response.json()['message']['width'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")
    
    def test_missing_one_args(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : "mm", "width" : 10.0, "length":10.0, "weight_unit": "g"})
        self.assertEqual(response.json()['message']['weight'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")
    
    def test_all_args_exist_width_str(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 'width', "length":10.0, "weight_unit": "g", "weight": 10.0})
        self.assertEqual(response.json()['message']['width'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")

    def test_arg_length_unit_not_mm_or_inches(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'm', "width" : 10.0, "length":10.0, "weight_unit": "g", "weight": 10.0})
        self.assertEqual(response.json()['message']['length_unit'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")
    
    def test_arg_weight_unit_not_g_or_ounces(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 10.0, "length":10.0, "weight_unit": "kg", "weight": 10.0})
        self.assertEqual(response.json()['message']['weight_unit'], "input json data format must include (str)length unit -> mm or inches , (float)width, (float)length, (str)weight unit -> g or ounces, (float)weight")

    def test_exceeds_length_limit(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 10.0, "length":400.0, "weight_unit": "g", "weight": 10.0})
        self.assertEqual(response.json()['message'], "length can not be larger than 380mm or 14.9606 inches")
    
    def test_exceeds_width_limit(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 300.0, "length":200.0, "weight_unit": "g", "weight": 10.0})
        self.assertEqual(response.json()['message'], "width can not be longer than 270mm or 10.6299 inches")
    
    def test_exceeds_weight_limit(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 100.0, "length":200.0, "weight_unit": "g", "weight": 600.0})
        self.assertEqual(response.json()['message'], "weight can not be heavier than 500g or 17.637 ounces")
    
    def test_standard_evolope(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 100.0, "length":200.0, "weight_unit": "g", "weight": 40.0})
        self.assertEqual(response.json()['message'], "the post_price is: 22.7")

    def test_non_standard_width_standard_length_standard_weight_evolope(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 200.0, "length":200.0, "weight_unit": "g", "weight": 40.0})
        self.assertEqual(response.json()['message'], "the post_price is: 39.2")
    
    def test_non_standard_length_standard_width_standard_weight_evolope(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 100.0, "length":300.0, "weight_unit": "g", "weight": 40.0})
        self.assertEqual(response.json()['message'], "the post_price is: 39.2")
    
    def test_non_standard_weight_standard_width_standard_length_evolope(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 100.0, "length":200.0, "weight_unit": "g", "weight": 100.0})
        self.assertEqual(response.json()['message'], "the post_price is: 98.0")
    
    def test_non_standard_large_weight_standard_width_standard_length_evolope(self):
        tester = app.test_client(self)
        response = requests.get(BASE + "calculator", {"length_unit" : 'mm', "width" : 100.0, "length":200.0, "weight_unit": "g", "weight": 120.0})
        self.assertEqual(response.json()['message'], "the post_price is: 146.0")
    

if __name__ == '__main__':
    unittest.main()