from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
sess = db.session

def addpackage():
    data = request.json
    # print(data)
    try:
        create_addpackage = table_package(name=data['package_name'] , price=data['package_price'] , counting=data['package_count'])
        sess.add(create_addpackage)
        sess.commit()
        sess.close()
        return json_response({"msg":"Createpackage success"}, 201)
    except :
        print("Create package Fail")
        sess.close()
        return json_response({"msg":"Fail"}, 400)



def getallpackage():
    data = []
    all_package = table_package.query.all()
    for i in all_package:
        data.append({"id":i.id , "package_name":i.name , "package_price":i.price , "package_count":i.counting})
    sess.close()
    return json_response(data)

def editpackage():
    data = request.json
    # print(data)
    # package_data = table_package.query.filter_by(id=data['id']).first()
    table_package.query.filter_by(id=data['id']).update({"name": data['package_name'] , "price":data['package_price'] , "counting":data['package_count']})
    sess.commit()
    sess.close()
    return json_response({"msg":"Update success"}, 201)

def deletepackage():
    package_id = request.args.get('package_id')
    package_data = table_package.query.filter_by(id=package_id).first()
    sess.delete(package_data)
    sess.commit()
    sess.close()
    return json_response({"msg": "delete success"}, 201)