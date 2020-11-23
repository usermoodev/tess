from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
sess = db.session

def add_admin():
    data = request.json

    username = data['username']
    password = data['password']
    email = data['email']
    phone = data['phone']
    company_id = data['company_id']
    if table_admin.query.filter_by(username=username).first() != None:
        sess.close()
        return json_response({"msg": "The username is already used"}, 401)
    else:
        create_admin = table_admin(username=username,
                                   password=encryption_password(password),
                                   email=email,
                                   phone=phone,
                                   role="admin",
                                   company_id=company_id)
        sess.add(create_admin)
        sess.commit()
        sess.close()
        return json_response({"msg": "Created admin success "}, 201)

def delete_admin():
    admin_id = request.args.get('admin_id')

    admin_data = table_admin.query.filter_by(id=admin_id).first()
    sess.delete(admin_data)
    sess.commit()
    sess.close()
    return json_response({"msg": "Delete admin success "}, 201)
def update_admin():
    data = request.json

    id = data['id']
    table_admin.query.filter_by(id=id).update({"username": data['username'] , "phone":data['phone'] ,"email":data['email'] })
    sess.commit()
    sess.close()
    return json_response({"msg":"update success"})

def addcompany():
    data = request.json

    username = data['username']
    password = data['password']
    email = data['email']
    phone = data['phone']

    package = data['package_name']
    package_data = table_package.query.filter_by(name=package).first()
    if table_admin.query.filter_by(username=username).first() != None:
        sess.close()
        return json_response({"msg": "The username is already used"}, 401)
    else:
        company_id = generate_uuid()
        create_company = table_company(id=company_id,
                                       name=data['company_name'],
                                       small_case=data['small_case'],
                                       medium_case=data['medium_case'],
                                       large_case=data['large_case'])
        sess.add(create_company)
        sess.commit()
        create_admin = table_admin(username=username,
                                   password=encryption_password(password),
                                   email=email,
                                   phone=phone,
                                   role="admin",
                                   company_id=company_id)
        sess.add(create_admin)
        sess.commit()
        create_company_package = table_company_package(company_id=company_id,
                                                       package_id=package_data.id
                                                       )
        sess.add(create_company_package)
        sess.commit()
        try:
            sendMail(company_name=data['company_name'] , username=username , password=password , emailto = email)

            return json_response({"msg": "Created company success "}, 201)
        except:
            print("sendmail error")

            return json_response({"msg": "Created company success "}, 201)
        sess.close()
    return json_response({"msg": "Fail Created company "}, 400)


def getallcompany():
    # try:
    data = []
    admin_id = request.args.get('admin_id')
    admin = table_admin.query.filter_by(id=admin_id).first()
    if admin != None:
        role = admin.role
        if role == "superadmin":
            # case superadmin
            all_company = table_company.query.all()
            for i in all_company:
                company_package_data = table_company_package.query.filter_by(company_id=i.id).first()
                package_data = table_package.query.filter_by(id=company_package_data.package_id).first()
                admin_data = table_admin.query.filter_by(company_id=i.id).first()
                data.append({"id":i.id,"company_name":i.name,"package_name":package_data.name , "phone":admin_data.phone ,"email":admin_data.email ,\
                             "small_case":i.small_case  , "medium_case":i.medium_case , "large_case":i.large_case})
            sess.close()
            return json_response(data)
        else:
            # case admin
            admin_data = table_admin.query.filter_by(id=admin_id).first()
            all_company = table_company.query.filter_by(id=admin_data.company_id).all()
            for i in all_company:
                company_package_data = table_company_package.query.filter_by(company_id=i.id).first()
                package_data = table_package.query.filter_by(id=company_package_data.package_id).first()
                admin_data = table_admin.query.filter_by(company_id=i.id).first()
                data.append(
                    {"id": i.id, "company_name": i.name, "package_name": package_data.name, "phone": admin_data.phone,
                     "email": admin_data.email})
            sess.close()
            return json_response(data)



def update_company():
    data = request.json
    # print(data)
    id = data['id']
    package = data['package_name']
    package_data = table_package.query.filter_by(name=package).first()
    table_company.query.filter_by(id=id).update({"name": data['company_name'] , "small_case":data['small_case']  , "medium_case":data['medium_case'] ,"large_case":data['large_case']})
    table_company_package.query.filter_by(company_id=id).update({"package_id": package_data.id})
    sess.commit()
    sess.close()
    return json_response({"msg": "update success"})


def delete_company():
    company_id = request.args.get('company_id')
    branch_data = table_branch.query.filter_by(company_id=company_id).all()
    company_data = table_company.query.filter_by(id=company_id).first()
    sess.delete(company_data)
    sess.commit()
    # if branch_data != None:
    #     sess.delete(company_data)

    #     sess.commit()
    sess.close()
    return json_response({"msg":"delete company success"})