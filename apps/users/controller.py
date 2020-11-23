from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
sess = db.session



def register_user():
    data = request.json
    # print(data)
    response = registercitizen_api(data)
    if response['result'] == "Fail":
        print("fail register")
        # print(response)
        errorcase = response['errorMessage']
        if "username" in errorcase:
            # print(response['errorMessage']['username'][0])
            sess.close()
            return json_response({'error':response['errorMessage']['username'][0]} , 400)
        else:
            print("not haskey username")
        sess.close()
        return json_response(response , 400)
    else:
        login_response = logincitizen(username=data['username'], password=data['password'])
        if login_response['result'] == "Fail":
            print("fail register in login one id")
            sess.close()
            return json_response(login_response , 400)
        else:
            one_id = login_response['account_id']
            # print ("response one_id" , one_id)
            create_users = table_users(username=data['username'],
                                       password=encryption_password(data['password']),
                                       account_title_th=data['account_title_th'],
                                       first_name_th=data['first_name_th'],
                                       last_name_th=data['last_name_th'],
                                       name=data['account_title_th']+ " " + data['first_name_th'] + " " + data['last_name_th'],
                                       phone=data['mobile_no'],
                                       email=data['email'],
                                       company_id=data['company_id'],
                                       branch_id=data['branch_id'],
                                       one_id=one_id
                                      )
            sess.add(create_users)
            sess.commit()
            sendMail_adduser(username=data['username'] , password=data['password'] , emailto=data['email'])
            print("success register")
            sess.close()
            return json_response(login_response,200)



def register_admin():
    data = request.json
    # print("data", data)
    username = data['username']
    password = data['password']
    email = data['email']
    phone = data['phone']
    if table_admin.query.filter_by(username=username).first() != None :
        sess.close()
        return json_response({"status": "The username is already used"}, 401)
    else:
        create_admin = table_admin(username=username,
                            password=encryption_password(password),
                            email=email,
                            phone=phone,
                            role="admin")
        sess.add(create_admin)
        sess.commit()
        sess.close()
        return json_response({"status": "Created admin {}".format(data['username'])}, 201)

def register_superadmin():
    data = request.json
    # print("data", data)
    username = data['username']
    password = data['password']
    email = data['email']
    phone = data['phone']
    if table_admin.query.filter_by(username=username).first() != None :
        sess.close()
        return json_response({"status": "The username is already used"}, 401)
    else:
        create_admin = table_admin(username=username,
                            password=encryption_password(password),
                            email=email,
                            phone=phone,
                            role="superadmin")
        sess.add(create_admin)
        sess.commit()
        sess.close()
        return json_response({"status": "Created superadmin {}".format(data['username'])}, 201)

def getallmember():
    company_id = request.args.get('company_id')
    admin = []
    user = []
    admin_data = table_admin.query.filter_by(company_id=company_id).all()
    company_data = table_company.query.filter_by(id=company_id).first()
    x = 1
    for i in admin_data:
        if i.role == "superadmin":
            pass
        else:
            admin.append({"id":i.id , "username":i.username,"phone":i.phone,"email":i.email , "company_name":company_data.name , "company_id":company_id})
    branch_data = table_branch.query.filter_by(company_id=company_data.id).all()
    for x in branch_data:
        user_data = table_users.query.filter_by(branch_id=x.id).all()
        for y in user_data:
             user.append({"user_id":y.id , "username":y.username, "account_title_th":y.account_title_th , "first_name_th":y.first_name_th , "last_name_th":y.last_name_th,
                          "name":y.name ,  "phone":y.phone , "email":y.email , "branch_name":x.name ,"company_name":company_data.name, "company_id":company_data.id})
    sess.close()
    return json_response({"admin":admin,"user":user})

def update_user():
    data = request.json
    # print(data)

    branch_data = table_branch.query.filter_by(name=data['branch_name'] , company_id=data['company_id']).first()
    table_users.query.filter_by(id=data['user_id']).update({"account_title_th":data['account_title_th'] ,
                                                            "first_name_th":data['first_name_th'],
                                                            "last_name_th":data['last_name_th'],
                                                            "name":data['account_title_th']+ " " + data['first_name_th'] + " " + data['last_name_th'],
                                                            "email":data['email'],
                                                            "phone":data['mobile_no'],
                                                            "branch_id":branch_data.id})
    sess.commit()
    sess.close()
    return json_response({"msg":"update user success"},201)

def delete_user():
    user_id = request.args.get('user_id')
    user_data = table_users.query.filter_by(id=user_id).first()
    sess.delete(user_data)
    sess.commit()
    sess.close()
    return json_response({"msg": "delete user success"}, 201)

def resetpassword_user():
    data = request.json

    # print(data)
    response = resetpassword_oneid(data=data)
    # print("resetpassword_user >> response",response)

    if response['result'] == "Fail":

        return json_response({"errorMessage":response['errorMessage']})
    else:

        return json_response(response)

def resetpassword_user_otp():
    data = request.json
    # print(data)

    response = resetpassword_by_otp(data=data)
    # print("resetpassword_user_otp >> response",response)
    if response['result'] == "Success":
        table_users.query.filter_by(username=data['username']).update({"password": encryption_password(data['new_password'])})
        sess.commit()
        sess.close()
        return json_response(response,200)
    else:
        sess.close()
        return json_response({"errorMessage":response['errorMessage']},400)
