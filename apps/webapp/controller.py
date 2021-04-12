from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
sess = db.session
from ..s3.s3 import *
import datetime
import shutil
import os

# import datetime


def cancel_edit():
    data = request.json
    closewebview(user_id=data['one_id'], bot_id=data['bot_id'])
    quickreply_edit(user_id=data['user_id'], bot_id=data['bot_id'], temp_id=data['temp_id'], one_id=data['one_id'],
                    lot_id=data['lot_id'])
    return json_response(data)
def aidetection():

    # webview case with unit
    user_id = request.args.get('user_id')
    one_id = request.args.get('one_id')
    lot_id = request.args.get('lot_id')
    # print("one_id",one_id)
    # print("lot_id" , lot_id)
    data = request.form
    licent = data['licent']
    # print(licent)
    length_wood = data['unit']
    print("type lenwood = ", type(length_wood))

    file = request.files['file']
    bot_id = request.args.get('bot_id')


    user_data = table_users.query.filter_by(onechat_id=user_id).first()
    if user_data == None:
        sent_text(user_id=user_id, messege="คุณไม่ได้รับอนุญาติให้ใช้ระบบ", bot_id=bot_id)
    else:
        company_data = table_company.query.filter_by(id=user_data.company_id).first()
        now = datetime.datetime.now()
        timenow = now + datetime.timedelta(minutes=7*60)
        now = timenow.strftime("date%d%m%Ytime%H%M%S%f")
        sent_text(user_id=user_id , messege="ได้รับภาพแล้วกำลังตรวจจับท่อนไม้" , bot_id=bot_id)
        filepath = photopath + str(user_id) + "/"
        if os.path.exists(filepath):
            print("remove folder")
            shutil.rmtree(filepath)
            print("create folder")
            os.makedirs(filepath)
        else:
            print("create folder")
            os.makedirs(filepath)

        filename = str(now) + ".png"
        fullpath = filepath+filename
        file.save(os.path.join(filepath,filename))
        print("save images in >> " , filepath+filename)
        s3_upload(path_file=fullpath, path_s3=path_s3, filename=filename)
        s3link_notdetect = s3_generatelink(s3_path=path_s3, filename=filename)
        base64code = createBase64webveiw(filepath=filepath,filename=filename)

        result = detecttimberwebveiw(base64=base64code,
                              small_case=company_data.small_case,
                              medium_case=company_data.medium_case,
                              large_case=company_data.large_case,
                              bot_id=bot_id,
                              length_wood=length_wood)
        resahape_img = result['data']['resahape_img']
        resahape_img_path = createimageswebveiw(resahape_img, "before" + str(now) + '.png' , user_id)
        s3_upload(path_file=resahape_img_path, path_s3=path_s3, filename="before" + str(now) + '.png')
        s3link_resahape_img = s3_generatelink(s3_path=path_s3, filename="before" + str(now) + '.png')

        images_detected = result['data']['result_img']
        images_detected_path = createimageswebveiw(images_detected, "plot"+str(now)+'.png' , user_id)
        s3_upload(path_file=images_detected_path, path_s3=path_s3, filename="plot"+str(now)+'.png')
        s3link_detect = s3_generatelink(s3_path=path_s3, filename="plot"+str(now)+'.png')
        small = result['data']['wood_count']['Small']
        medium = result['data']['wood_count']['Medium']
        large = result['data']['wood_count']['Large']
        total = result['data']['wood_count']['Total']
        discard = result['data']['wood_count']['Discard']
        small_volume = result['data']['wood_volume']['Small']
        medium_volume = result['data']['wood_volume']['Medium']
        large_volume = result['data']['wood_volume']['Large']
        discard_volume = result['data']['wood_volume']['Discard']
        total_volume = result['data']['wood_volume']['Total']

        # print(small_volume , medium_volume  ,large_volume ,discard_volume ,total_volume)

        sent_image(user_id=user_id, bot_id=bot_id, fullpath=resahape_img_path)
        sent_image(user_id=user_id, bot_id=bot_id, fullpath=images_detected_path)

        now = datetime.datetime.now()
        timenow = now + datetime.timedelta(minutes=7 * 60)
        date = timenow.strftime("%d/%m/%Y ")
        timenow_ = timenow.strftime("%H:%M ")

        if table_lot.query.filter_by(id=lot_id).first() == None:
            createLot = table_lot(id=lot_id,
                                  company_id=user_data.company_id,
                                  branch_id=user_data.branch_id,
                                  users_id=user_data.id,
                                  dateupload=timenow,
                                  license_plate = licent)
            sess.add(createLot)
        branchData = table_branch.query.filter_by(id=user_data.branch_id).first()


        sent_text(user_id, "วันที่ " + date +
                  "\nเวลา " + timenow_ + "น." +
                  "\nชื่อสาขา " + branchData.name +
                  "\nชื่อผู้ใช้งาน " + user_data.username +
                  "\n   *** Lot หมายเลข *** " +
                  "\n  " + lot_id +
                  "\n   ********************* " +
                  "\nเลขทะเบียน/เลขคิว : " + licent +
                  "\nเกณฑ์ไม้เล็ก : >= " + company_data.small_case + "\"" +
                  "\nเกณฑ์ไม้กลาง : >= " + company_data.medium_case +"\"" +
                  "\nเกณฑ์ไม้ใหญ่ : >= " + company_data.large_case + "\"" +
                  "\n   *******************" +
                  "\nไม้เล็ก : " + str(small) + " ท่อน" +
                  "\nไม้กลาง : " + str(medium) + " ท่อน" +
                  "\nไม้ใหญ่ : " + str(large) + " ท่อน" +
                  "\nไม่ถึงเกณฑ์ : "+ str(discard) + " ท่อน" +
                  "\nจำนวนไม้ทั้งหมด : " + str(total) + " ท่อน" +
                  "\n   *******************" +
                  '\nไม้เล็ก : '+ str(small_volume) + ' m³' +
                  '\nไม้กลาง : '+ str(medium_volume) + ' m³' +
                  '\nไม้ใหญ่ : '+ str(large_volume) + ' m³' +
                  '\nไม้ทั้งหมด : '+ str(total_volume) + ' m³' ,
                  bot_id)
        temp_id = generate_uuid()
        length_wood = float(length_wood)
        print("type lenwood 2 = ", type(length_wood))
        create_temp = table_temp_history(id=temp_id,
                                        users_id=user_data.id,
                                       company_id=user_data.company_id,
                                       branch_id=user_data.branch_id,
                                       small_wood=small,
                                       medium_wood=medium,
                                       large_wood=large,
                                       total_wood=total,
                                       total_wood_edit=total,
                                       discard_wood=discard,
                                       original_pic=s3link_resahape_img,
                                       detected_pic=s3link_detect,
                                       dateupload=timenow,
                                       small_volume=small_volume,
                                       medium_volume=medium_volume,
                                       large_volume=large_volume,
                                       total_volume=total_volume,
                                       small_volume_edit =small_volume,
                                       medium_volume_edit = medium_volume,
                                       large_volume_edit = large_volume,
                                       total_volume_edit = total_volume,
                                       onechat_id=user_id,
                                       comment = "",
                                       lot_id=lot_id,
                                       license_plate=licent,
                                       length_wood=length_wood,
                                       backup_pic=s3link_notdetect)
        sess.add(create_temp)
        sess.commit()
        closewebview(user_id=one_id, bot_id=bot_id)
        quickreply_inprocess(user_id=user_id , bot_id=bot_id , temp_id=temp_id , one_id=one_id , lot_id=lot_id)

        # try:
        #     print("remove file in  = ", fullpath)
        #     os.remove(resahape_img_path)
        #     os.remove(images_detected_path)
        #     os.remove(fullpath)
        # except:
        #     print("error remove")

    sess.close()
    return json_response({"msg":"success"})

def gettemp():
    temp_id = request.args.get('temp_id')
    print("web view get temp = " , temp_id)
    jstr = []
    temp_data = table_temp_history.query.filter_by(id=temp_id).first()
    small = None
    medium = None
    large = None
    if temp_data.small_wood_edit == None:
        small = temp_data.small_wood
    else:
        small = temp_data.small_wood_edit

    if temp_data.medium_wood_edit == None:
        medium = temp_data.medium_wood
    else:
        medium = temp_data.medium_wood_edit

    if temp_data.large_wood_edit == None:
        large = temp_data.large_wood
    else:
        large = temp_data.large_wood_edit


    # print(temp_data)
    sess.close()
    return json_response({"temp_id":temp_data.id ,
                          "small_wood":small ,
                          "medium_wood":medium ,
                          "large_wood":large,
                          "company_id":temp_data.company_id
                          })

def edittemp():
    data = request.json
    # print(data)
    closewebview(user_id=data['one_id'] , bot_id=data['bot_id'])

    temp_data = table_temp_history.query.filter_by(id=data['temp_id']).first()
    case_data = table_company.query.filter_by(id=temp_data.company_id).first()

    small_case = case_data.small_case
    medium_case = case_data.medium_case
    large_case = case_data.large_case
    # print(small_case , medium_case , large_case)
    # print(temp_data.length_wood)
    # wood_diameter_inch = ความยาวหน้าตัดหน่วยนิ้ว
    # wood_diameter_meter = (wood_diameter_inch * 2.54) / 100.0
    # volume = ((3.14 * pow(wood_diameter_meter, 2)) / 4.0) * float(length_wood)
    before_small_wood = temp_data.small_wood
    before_medium_wood = temp_data.medium_wood
    before_large_wood = temp_data.large_wood
    before_s_volume = temp_data.small_volume
    before_m_volume = temp_data.medium_volume
    before_l_volume = temp_data.large_volume
    before_t_volume = temp_data.total_volume

    small_volume = 0
    medium_volume = 0
    large_volume = 0


    wood_diameter_inch_small_case = float(small_case)
    wood_diameter_meter_small_case = (wood_diameter_inch_small_case * 2.54) / 100.0
    small_volume = (((3.14 * pow(wood_diameter_meter_small_case, 2)) / 4.0) * float(temp_data.length_wood))

    wood_diameter_inch_medium_case = float(medium_case)
    wood_diameter_meter_medium_case = (wood_diameter_inch_medium_case * 2.54) / 100.0
    medium_volume = (((3.14 * pow(wood_diameter_meter_medium_case, 2)) / 4.0) * float(temp_data.length_wood))

    wood_diameter_inch_large_case = float(large_case)
    wood_diameter_meter_large_case = (wood_diameter_inch_large_case * 2.54) / 100.0
    large_volume = (((3.14 * pow(wood_diameter_meter_large_case, 2)) / 4.0) * float(temp_data.length_wood))
    # print(small_volume  , medium_volume , large_volume)
    table_temp_history.query.filter_by(id=data['temp_id']).update({"small_wood_edit": data['small_wood'] ,
                                                                   "medium_wood_edit":data['medium_wood'],
                                                                   "large_wood_edit":data['large_wood'],
                                                                   "small_volume_edit":small_volume,
                                                                   "medium_volume_edit":medium_volume,
                                                                   "large_volume_edit": large_volume,
                                                                   "total_volume_edit":small_volume+medium_volume+large_volume,
                                                                   "total_wood_edit":float(data['small_wood'])+float(data['medium_wood'])+float(data['large_wood']),
                                                                   "comment":str(data['comment'])})
    sess.commit()

    sent_text(user_id=data['user_id'] , bot_id=data['bot_id'] , messege=" ********************** " +
                                                                        "\n     ข้อมูลถูกแก้ไขเป็น" +
                                                                        "\n ********************** " +
                                                                        "\nไม้เล็ก : " + str(data['small_wood']) +
                                                                        "\nไม้กลาง : "  + str(data['medium_wood']) +
                                                                        "\nใหญ่ : " + str(data['large_wood']) +
                                                                        "\nสาเหตุที่แก้ : " + str(data['comment'])
              )
    quickreply_edit(user_id=data['user_id'], bot_id=data['bot_id'], temp_id=data['temp_id'], one_id=data['one_id'], lot_id=data['lot_id'])

    sess.close()
    # quickreply(user_id=data['user_id'] , bot_id=data['bot_id'] , temp_id=data['temp_id'] , one_id=data['one_id'])
    return json_response({"msg":"ok"})