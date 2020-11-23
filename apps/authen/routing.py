# -*- coding: utf-8 -*
from apps.authen import controller
from ..helper.helper import *
print ('...start routing module api')
from flask import Blueprint
import string
import random
from pandas import DataFrame
routes = Blueprint('/authen',__name__)

routes.add_url_rule(
    '',
    '',
    controller.login,
    methods = ['POST']
)
routes.add_url_rule(
    'forgetpassword',
    'forgetpassword',
    controller.forgetpassword,
    methods = ['POST']
)

# sendMail(company_name="7-11" , username="หรั่ง" , password="เทพมาก")
# print("password = " ,encryption_password("timber07"))
# letters = string.ascii_lowercase
# randompassword = ''.join(random.choice(letters) for i in range(8))
# encrypt_randompassword = encryption_password(randompassword)

# mylist = ["bangkok", "lampang", "lamphun" , "ayutthaya"]
# list = [{"id":"123" , "branch_name":"bangkok" ,"user_name":"user_bangkok"} ,
#         {"id":"123" , "branch_name":"lampang" ,"user_name":"user_lampang"},
#         {"id":"123" , "branch_name":"lamphun" ,"user_name":"user_bangkok"},
#         {"id":"123" , "branch_name":"ayutthaya" ,"user_name":"user_ayutthaya"}]
#
# branch = []
#
# for i  in range(len(list)):
#     print(list[i]['branch_name'])
#     if list[i]['branch_name'] in branch:
#         pass
#     else:
#         branch.append(list[i]['branch_name'])
#
#
# print(branch)
# date_time_str = '24/02/2020'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%d/%m/%Y')
# print(date_time_obj)
# print(type(date_time_obj))

# cars = {'ไฟฟ้า': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#         'น้ำ': [22000,25000,27000,35000]
#         }
#
# df = DataFrame(cars, columns= ['ไฟฟ้า', 'น้ำ'])
#
# print (df)
# export_csv = df.to_csv (r'D:/inet/wood_detection/export_dataframe.csv', index = None, header=True , encoding='utf-8-sig')

print ('...finish routing module api222')