from flask import request ,Response , json ,send_file
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
from sqlalchemy import and_
sess = db.session
from datetime import *
import datetime
# import datetime


def getlot():

    branch_id = request.args.get("branch_id")
    startdate = request.args.get("date_start")
    enddate = request.args.get("date_end")
    all_branch = branch_id.split(',')
    date_format = "%d/%m/%Y"
    checkdate = 0
    try:
        ifstart = datetime.datetime.strptime(startdate, date_format)
        ifend =  datetime.datetime.strptime(enddate, date_format)
        ifend = ifend + datetime.timedelta(days=1)
        all_branch = branch_id.split(',')
        checkdate = 1
    except:
        checkdate = 0

    data = []



    for x in range(len(all_branch)):
        if checkdate == 1 :
            lot_data = table_lot.query.filter_by(branch_id=all_branch[x]).order_by(table_lot.dateupload.desc()).filter(table_lot.dateupload <= ifend).filter(table_lot.dateupload >=ifstart).all()
        else:
            lot_data = table_lot.query.filter_by(branch_id=all_branch[x]).order_by(table_lot.dateupload.desc()).all()
        if lot_data == []:

            print("No history")
            pass
        else:
            for i in range (len(lot_data)):
                # print(lot_data[i])
                company_data = table_company.query.filter_by(id=lot_data[i].company_id).first()
                # print("company_data" , company_data)
                branch_data = table_branch.query.filter_by(id=lot_data[i].branch_id).first()
                # print("branch_data" , branch_data)
                user_data = table_users.query.filter_by(id=lot_data[i].users_id).first()
                # print("user_data",user_data)
                # print("lot_data[i]" , lot_data[i].id)
                history_data = table_history.query.filter_by(lot_id=lot_data[i].id).all()
                # print(history_data)
                history_sub = []
                if history_data == []:
                    print("pass")
                    pass
                else:
                    for g in range (len(history_data)):
                        # print(history_data[g])
                        datetime_nowhistory = history_data[g].dateupload.strftime("%d/%m/%Y %H:%M")
                        if history_data[g].comment == "" :
                            small_wood = history_data[g].small_wood
                            medium_wood = history_data[g].medium_wood
                            large_wood = history_data[g].large_wood
                            total_wood = history_data[g].total_wood
                        else:
                            small_wood = history_data[g].small_wood_edit
                            medium_wood = history_data[g].medium_wood_edit
                            large_wood = history_data[g].large_wood_edit
                            total_wood = history_data[g].total_wood_edit
                        history_sub.append({"history_id":history_data[g].id ,
                             "username":user_data.username , "name":user_data.name ,
                             "branch_id":branch_data.id , "branch_name":branch_data.name,
                             "company_id":company_data.id , "company_name":company_data.name ,
                             "small_wood":small_wood , "medium_wood":medium_wood , "large_wood":large_wood, "total_wood":total_wood ,"discard_wood":history_data[g].discard_wood,
                             "original_pic":history_data[g].original_pic , "detected_pic":history_data[g].detected_pic ,
                             "date":datetime_nowhistory , "small_volume":history_data[g].small_volume , "medium_volume":history_data[g].medium_volume , "large_volume":history_data[g].large_volume ,"total_volume":history_data[g].total_volume})

                datetime_now = lot_data[i].dateupload.strftime("%d/%m/%Y %H:%M")
                data.append({"lot_id":lot_data[i].id ,
                             "username":user_data.username , "name":user_data.name ,
                             "branch_id":branch_data.id , "branch_name":branch_data.name,
                             "company_id":company_data.id , "company_name":company_data.name ,
                             "small_wood":lot_data[i].small_wood , "medium_wood":lot_data[i].medium_wood , "large_wood":lot_data[i].large_wood, "total_wood":lot_data[i].total_wood ,"discard_wood":lot_data[i].discard_wood,
                             "date":datetime_now , "small_volume":lot_data[i].small_volume , "medium_volume":lot_data[i].medium_volume , "large_volume":lot_data[i].large_volume ,"total_volume":lot_data[i].total_volume,
                             "license_plate":lot_data[i].license_plate , "history":history_sub})
    sess.close()
    return json_response(data)


def getdetailhistory():
    history_id = request.args.get("history_id")
    history_data = table_history.query.filter_by(id=history_id).first()

    if history_data == None:
        sess.close()
        return json_response({"msg":"ไม่พบ history" },400)
    else:
        company_data = table_company.query.filter_by(id=history_data.company_id).first()
        branch_data = table_branch.query.filter_by(id=history_data.branch_id).first()
        user_data = table_users.query.filter_by(id=history_data.users_id).first()
        datetime_now = history_data.dateupload.strftime("%d/%m/%Y %H:%M")
        if history_data.comment == "":
            small_wood = history_data.small_wood
            medium_wood = history_data.medium_wood
            large_wood = history_data.large_wood
            total_wood = history_data.total_wood
        else:
            small_wood = history_data.small_wood_edit
            medium_wood = history_data.medium_wood_edit
            large_wood = history_data.large_wood_edit
            total_wood = history_data.total_wood_edit
        data = {"history_id": history_data.id,
                "username": user_data.username, "name": user_data.name,
                "branch_id": branch_data.id, "branch_name": branch_data.name,
                "company_id": company_data.id, "company_name": company_data.name,
                "small_wood": history_data.small_wood, "medium_wood": history_data.medium_wood, "large_wood": history_data.large_wood,
                "total_wood": history_data.total_wood, "discard_wood": history_data.discard_wood, "discard_wood_edit":history_data.discard_wood,
                "small_wood_edit": small_wood, "medium_wood_edit": medium_wood,
                "large_wood_edit": large_wood, "total_wood_edit": history_data.total_wood_edit,
                "comment":history_data.comment ,
                "original_pic": history_data.original_pic, "detected_pic": history_data.detected_pic,
                "date": datetime_now,
                "small_volume": history_data.small_volume, "medium_volume": history_data.medium_volume,"large_volume": history_data.large_volume,
                "total_volume": history_data.total_volume,
                "small_volume_edit":history_data.small_volume_edit , "medium_volume_edit":history_data.medium_volume_edit , "large_volume_edit":history_data.large_volume_edit,
                "total_volume_edit":history_data.total_volume_edit,
                "lot_id":history_data.lot_id , "license_plate":history_data.license_plate
                }
        sess.close()
        return json_response(data,200)


def detaillot():
    lot_id = request.args.get("lot_id")
    # print(lot_id)
    data = []
    history_data = table_history.query.filter_by(lot_id=lot_id).all()
    if history_data == []:
        sess.close()
        return json_response({"msg":"ยังไม่มีผลการตรวจจับของ Lot นี้" },400)
    else:
        for i in history_data:
            company_data = table_company.query.filter_by(id=i.company_id).first()
            branch_data = table_branch.query.filter_by(id=i.branch_id).first()
            user_data = table_users.query.filter_by(id=i.users_id).first()
            datetime_now = i.dateupload.strftime("%d/%m/%Y %H:%M")
            data.append({"history_id":i.id ,
                         "username":user_data.username , "name":user_data.name ,
                         "branch_id":branch_data.id , "branch_name":branch_data.name,
                         "company_id":company_data.id , "company_name":company_data.name ,
                         "small_wood":i.small_wood , "medium_wood":i.medium_wood , "large_wood":i.large_wood, "total_wood":i.total_wood ,"discard_wood":i.discard_wood,
                         "original_pic":i.original_pic , "detected_pic":i.detected_pic ,
                         "date":datetime_now , "small_volume":i.small_volume , "medium_volume":i.medium_volume , "large_volume":i.large_volume ,"total_volume":i.total_volume})
    sess.close()
    return json_response(data)

def gethistorysuperadmin():

    # company_id = request.args.get("company_id")
    # history_data = table_history.query.filter_by(company_id=company_id).order_by(table_history.dateupload.desc()).all()
    # data = []
    # for i in history_data:
    #     company_data = table_company.query.filter_by(id=i.company_id).first()
    #     branch_data = table_branch.query.filter_by(id=i.branch_id).first()
    #     user_data = table_users.query.filter_by(id=i.users_id).first()
    #     datetime_now = i.dateupload.strftime("%d/%m/%Y %H:%M")
    #     data.append({"history_id":i.id ,
    #                  "username":user_data.username , "name":user_data.name ,
    #                  "branch_id":branch_data.id , "branch_name":branch_data.name,
    #                  "company_id":company_data.id , "company_name":company_data.name ,
    #                  "small_wood":i.small_wood , "medium_wood":i.medium_wood , "large_wood":i.large_wood, "total_wood":i.total_wood ,"discard_wood":i.discard_wood,
    #                  "original_pic":i.original_pic , "detected_pic":i.detected_pic ,
    #                  "date":datetime_now , "small_volume":i.small_volume , "medium_volume":i.medium_volume , "large_volume":i.large_volume ,"total_volume":i.total_volume})
    # return json_response(data)
    company_id = request.args.get("company_id")
    all_branch = []
    branch_data = table_branch.query.filter_by(company_id=company_id).all()
    for i in range(len(branch_data)):
        all_branch.append(branch_data[i].id)

    # print(all_branch)
    data = []
    history_sub = []
    for x in range(len(all_branch)):
        lot_data = table_lot.query.filter_by(branch_id=all_branch[x]).order_by(table_lot.dateupload.desc()).all()
        if lot_data == []:
            get_branch = table_branch.query.filter_by(id=all_branch[x]).first()
            pass
        else:
            for i in range (len(lot_data)):
                # print(lot_data[i])
                company_data = table_company.query.filter_by(id=lot_data[i].company_id).first()
                # print("company_data" , company_data)
                branch_data = table_branch.query.filter_by(id=lot_data[i].branch_id).first()
                # print("branch_data" , branch_data)
                user_data = table_users.query.filter_by(id=lot_data[i].users_id).first()
                # print("user_data",user_data)
                # print("lot_data[i]" , lot_data[i].id)
                history_data = table_history.query.filter_by(lot_id=lot_data[i].id).all()
                # print(history_data)
                history_sub = []
                if history_data == []:
                    print("pass")
                    pass
                else:

                    for g in range (len(history_data)):
                        print(history_data[g])
                        datetime_nowhistory = history_data[g].dateupload.strftime("%d/%m/%Y %H:%M")
                        if history_data[g].comment == "" :
                            small_wood = history_data[g].small_wood
                            medium_wood = history_data[g].medium_wood
                            large_wood = history_data[g].large_wood
                            total_wood = history_data[g].total_wood
                        else:
                            small_wood = history_data[g].small_wood_edit
                            medium_wood = history_data[g].medium_wood_edit
                            large_wood = history_data[g].large_wood_edit
                            total_wood = history_data[g].total_wood_edit
                        history_sub.append({"history_id":history_data[g].id ,
                             "username":user_data.username , "name":user_data.name ,
                             "branch_id":branch_data.id , "branch_name":branch_data.name,
                             "company_id":company_data.id , "company_name":company_data.name ,
                             "small_wood":small_wood , "medium_wood":medium_wood , "large_wood":large_wood, "total_wood":total_wood ,"discard_wood":history_data[g].discard_wood,
                             "original_pic":history_data[g].original_pic , "detected_pic":history_data[g].detected_pic ,
                             "date":datetime_nowhistory , "small_volume":history_data[g].small_volume , "medium_volume":history_data[g].medium_volume , "large_volume":history_data[g].large_volume ,"total_volume":history_data[g].total_volume})

                datetime_now = lot_data[i].dateupload.strftime("%d/%m/%Y %H:%M")
                data.append({"lot_id":lot_data[i].id ,
                             "username":user_data.username , "name":user_data.name ,
                             "branch_id":branch_data.id , "branch_name":branch_data.name,
                             "company_id":company_data.id , "company_name":company_data.name ,
                             "small_wood":lot_data[i].small_wood , "medium_wood":lot_data[i].medium_wood , "large_wood":lot_data[i].large_wood, "total_wood":lot_data[i].total_wood ,"discard_wood":lot_data[i].discard_wood,
                             "date":datetime_now , "small_volume":lot_data[i].small_volume , "medium_volume":lot_data[i].medium_volume , "large_volume":lot_data[i].large_volume ,"total_volume":lot_data[i].total_volume,
                             "license_plate":lot_data[i].license_plate , "history":history_sub})
    if data == []:
        sess.close()
        return json_response({"msg":"บริษัทที่ท่านเลือก ยังไม่มี log"},400)
    sess.close()
    return json_response(data)

def exportcsv():
    data = request.json
    company_id = data['company_id']
    timstart = datetime.datetime.strptime(data['date_start'], '%d/%m/%Y')
    timeend = datetime.datetime.strptime(data['date_end'], '%d/%m/%Y')


    now = timstart
    branch_name = data['branch_name']
    timeend += datetime.timedelta(minutes=(24 * 60)-1)
    company_data = table_company.query.filter_by(id=company_id).first()
    log = []
    name = []
    branch = []
    company = []
    small_wood = []
    medium_wood = []
    large_wood = []
    discard_wood = []
    total_wood = []
    small_volume = []
    medium_volume = []
    large_volume = []
    total_volume = []
    dateupload = []

    for bracnh_i in range(len(branch_name)):
        branch_data = table_branch.query.filter_by(company_id=data['company_id'] , name=branch_name[bracnh_i]).first()
        xlsx = table_history.query.filter_by(company_id=data["company_id"], branch_id=branch_data.id).filter(
            and_(table_history.dateupload >= timstart, table_history.dateupload <= timeend) , table_history.lot_id != None).order_by(
            table_history.dateupload.desc()).all()
        for x in xlsx:
            user_data = table_users.query.filter_by(id=x.users_id).first()
            name.append(user_data.name)
            branch.append(branch_name[bracnh_i])
            company.append(company_data.name)
            small_wood.append(x.small_wood)
            medium_wood.append(x.medium_wood)
            large_wood.append(x.large_wood)
            discard_wood.append(x.discard_wood)
            total_wood.append(x.total_wood)
            dateupload.append(x.dateupload)
            small_volume.append(x.small_volume)
            medium_volume.append(x.medium_volume)
            large_volume.append(x.large_volume)
            total_volume.append(x.total_volume)
            log.append({"user": user_data.name, "branch": branch_name[bracnh_i], "company": company_data.name,
                        "small_wood": x.small_wood,
                        "medium_wood": x.medium_wood,
                        "large_wood": x.large_wood,
                        "discard_wood": x.discard_wood,
                        "total_wood": x.total_wood,
                        "small_volume": x.small_volume,
                        "medium_volume": x.medium_volume,
                        "large_volume": x.large_volume,
                        "date": x.dateupload})


    fromdata = {'ผู้ใช้งาน': name,
                'บริษัท': company,
                'สาขา':branch,
                "ไม้เล็ก":small_wood,
                "ไม้กลาง":medium_wood,
                "ไม้ใหญ่":large_wood,
                "ไม่ถึงเกณฑ์":discard_wood,
                "จำนวนทั้งหมด":total_wood,
                "ปริมาตรไม้เล็ก(ลูกบาศก์เมตร)":small_volume,
                "ปริมาตรไม้กลาง(ลูกบาศก์เมตร)":medium_volume,
                "ปริมาตรไม้ใหญ่(ลูกบาศก์เมตร)":large_volume,
                "ปริมาตรไม้ทั้งหมด(ลูกบาศก์เมตร)":total_volume,
                "เวลา":dateupload}

    df = DataFrame(fromdata, columns=['ผู้ใช้งาน', 'บริษัท' ,'สาขา' ,'ไม้เล็ก','ไม้กลาง','ไม้ใหญ่' , 'ไม่ถึงเกณฑ์' , 'จำนวนทั้งหมด',  'ปริมาตรไม้เล็ก(ลูกบาศก์เมตร)' ,'ปริมาตรไม้กลาง(ลูกบาศก์เมตร)', 'ปริมาตรไม้ใหญ่(ลูกบาศก์เมตร)' ,'ปริมาตรไม้ทั้งหมด(ลูกบาศก์เมตร)', 'เวลา'])

    fullpath = export_path+"report"+".csv"
    export_csv = df.to_csv(fullpath, index=None, header=True, encoding='utf-8-sig')
    sess.close()
    return send_file(fullpath, attachment_filename="report"+".csv")

def getuser():
    data = request.json
    jstr = []
    # print(data)
    if data['branch_name'] == "ALL":
        sess.close()
        return json_response(jstr)
    else:
        branch_data = table_branch.query.filter_by(name=data['branch_name']).first()
        user_data = table_users.query.filter_by(branch_id=branch_data.id , company_id=data['company_id']).all()
        for i in user_data:
            jstr.append({"name":i.name})
        sess.close()
        return json_response(jstr)
