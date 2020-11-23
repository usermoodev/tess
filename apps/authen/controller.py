from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
import string , random
sess = db.session


def login():
    data = request.json
    # print(data)
    checkdata = table_admin.query.filter_by(username=data['username']).first()
    if checkdata == None:
        sess.close()
        return json_response({"msg": "username or password incorect"},401)

    if data['username'] == checkdata.username and encryption_password(data['password']) == checkdata.password:
        # if data['username'] == checkdata.username and data['password'] == checkdata.password:
        token = genToken(data['username'])
        table_admin.query.filter_by(username=data['username']).update({"access_token": token})
        sess.commit()
        company_data = table_company.query.filter_by(id=checkdata.company_id).first()
        # print({"status": "Success",
        #                       "admin_id":checkdata.id,
        #                       "access_token": token,
        #                       "username": checkdata.username,
        #                       "role": checkdata.role,
        #                       "company_name":company_data.name,
        #                       "company_id":company_data.id})
        sess.close()
        return json_response({"status": "Success",
                              "admin_id": checkdata.id,
                              "access_token": token,
                              "username": checkdata.username,
                              "role": checkdata.role,
                              "company_name":company_data.name,
                              "company_id":company_data.id}, 200)

    else:
        sess.close()
        return json_response({"msg": "username or password incorect"}, 401)

def forgetpassword():
    data = request.json
    email = data['email']
    username = data['username']

    admin_data = table_admin.query.filter_by(email=email , username=username).first()
    if admin_data == None:
        sess.close()
        return json_response({"msg": "username และ email ในระบบไม่ตรงกัน"},400)

    else:
        letters = string.ascii_lowercase
        randompassword = ''.join(random.choice(letters) for i in range(8))
        encrypt_randompassword = encryption_password(randompassword)
        # print("randompassword",randompassword)
        # print("encrypt_randompassword", encrypt_randompassword)
        table_admin.query.filter_by(username=username, email=email).update({'password': encrypt_randompassword})
        sess.commit()
        sendMailForgetpassword(data=data , randompassword = randompassword)
        sess.close()
        return json_response({"msg":"reset password success"},201)