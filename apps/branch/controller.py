from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
sess = db.session

def addbranch():
    data = request.json
    # print(data)

    branch_data = table_branch.query.filter_by(company_id=data['company_id'] , name=data['branch_name']).first()
    if branch_data == None:
        try:
            create_addbranch = table_branch(name=data['branch_name'],
                                            address=data['branch_address'],
                                            phone=data['branch_phone'],
                                            company_id=data['company_id'])
            sess.add(create_addbranch)
            sess.commit()
            sess.close()
            return json_response({"msg":"create branch success"}, 201)
        except:
            print("fail create branch ")
            sess.close()
            return json_response({"msg":"fail create branch "}, 400)
    else:
        sess.close()
        return json_response({"msg":"ชื่อสาขาของท่านซ้ำแล้ว"},400)

def getallbranch():
    company_id = request.args.get('company_id')
    data = []
    branch_data = table_branch.query.filter_by(company_id=company_id).all()
    for i in branch_data:
        data.append({"branch_id":i.id , "branch_name":i.name , "branch_phone":i.phone , "branch_address":i.address})
    sess.close()
    return json_response(data)

def deletebranch():
    branch_id = request.args.get('branch_id')
    branch_data = table_branch.query.filter_by(id=branch_id).first()
    sess.delete(branch_data)
    sess.commit()
    sess.close()
    return json_response({"msg": "delete branch success"}, 201)

def editbranch():
    data = request.json
    # print(data)
    branch_data = table_branch.query.filter_by(id=data['branch_id']).first()
    if branch_data is not None:
        table_branch.query.filter_by(id=data['branch_id']).update({"name": data['branch_name'], "address": data['branch_address'], "phone": data['branch_phone']})
        sess.commit()
        sess.close()
        return json_response({"msg": "update branch success"}, 201)
    else:
        sess.close()
        return json_response({"msg": "แก้ไขสาขาไม่สำเร็จ"}, 400)
