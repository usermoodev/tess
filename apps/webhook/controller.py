from flask import request ,Response , json
from apps.app import *
from apps.database import *
import requests
from ..helper.helper import *
import datetime
import random
sess = db.session
from ..s3.s3 import *

def webhook():
    data = request.json
    # print(data)


    # text = {'source': {'display_name': 'timber01@one.th',
    #                    'type_source': 'user',
    #                    'user_id': 'U2428568d44db532c8d7ecb50946fa5fe',
    #                    'email': 'timber01@one.th'},
    #         'timestamp': 1582175162000,
    #         'message': {'text': 'p', 'type': 'text',
    #                     'id': '5e4e13ba2d425d00293194b3'},
    #         'event': 'message',
    #         'bot_id': 'B3115ba2f981b59b69f38856e44119197'}
    # photo = {'source': {'display_name': 'timber01@one.th',
    #                     'type_source': 'user',
    #                     'user_id': 'U2428568d44db532c8d7ecb50946fa5fe',
    #                     'email': 'timber01@one.th'},
    #          'timestamp': 1582175317000,
    #          'message': {'type': 'image', 'id': '5e4e1455f3518c002bab9983',
    #                      'file': 'https://c88_05:08:36:773058.jpeg'},
    #          'event': 'message',
    #          'bot_id': 'B3115ba2f981b59b69f38856e44119197'}

    # addfriend = {'source': {'type_souce': 'user',
    #                         'display_name': 'timber01@one.th',
    #                         'one_id': '25313489504',
    #                         'user_id': 'U2428568d44db532c8d7ecb50946fa5fe',
    #                         'email': 'timber01@one.th'},
    #              'timestamp': 1582175683000,
    #              'event': 'add_friend',
    #              'bot_id': 'B3115ba2f981b59b69f38856e44119197'}

    # quickreplymsg = {'source': {'display_name': 'jarindeveloper@one.th',
    #                             'one_id': '3148142722',
    #                             'type_source': 'user',
    #                             'user_id': 'U46caf077e7e05e9c902f15f7a7959a83',
    #                             'email': 'jarin.kh@one.th'},
    #                  'timestamp': 1583392736000,
    #                  'message': {'text': 'ฉันต้องยืนยัน',
    #                              'type': 'text',
    #                              'id': '5e60a7e03af918002915d6e4',
    #                              'data': {'service': '001',
    #                                       'confirm': 'lotID'}},
    #                  'event': 'message',
    #                  'bot_id': 'B3115ba2f981b59b69f38856e44119197'}

    # webhook with webview
    # print(data)
    if data['event'] == "add_friend":
        one_id = data['source']['one_id']
        user_id = data['source']['user_id']
        bot_id = data['bot_id']
        user_data = table_users.query.filter_by(one_id=one_id).first()
        if user_data == None:
            sent_text(user_id=user_id , messege="คุณไม่ได้รับอนุญาติให้ใช้ระบบ" , bot_id=bot_id)
        else:
            company_data = table_company.query.filter_by(id=user_data.company_id).first()
            branch_data = table_branch.query.filter_by(id=user_data.branch_id).first()
            sent_text(user_id=user_id, messege="การยืนยันตัวตนสำเร็จ\nยินดีต้อนรับคุณ {} \nบริษัท {} \nสาขา {}".format(user_data.first_name_th , company_data.name,branch_data.name), bot_id=bot_id)
            table_users.query.filter_by(one_id=one_id).update({"onechat_id": user_id})
            sess.commit()

            # sand_template(user_id=user_id , bot_id=bot_id)
    elif data['event']  == "message":
        user_id = data['source']['user_id']
        one_id = data['source']['one_id']
        bot_id = data['bot_id']
        user_data = table_users.query.filter_by(onechat_id=user_id).first()
        if user_data == None:
            sent_text(user_id=user_id, messege="คุณไม่ได้รับอนุญาติให้ใช้ระบบ", bot_id=bot_id)
        else:
            if data['message']['type'] == 'text':
                if 'data' in data['message']:
                    print("from quick replay")
                    if 'confirm' in data['message']['data']:
                        print("case confirm")
                        temp_data = table_temp_history.query.filter_by(id=data['message']['data']['confirm']).first()
                        create_history = table_history(id=temp_data.id,
                                                         users_id=temp_data.users_id,
                                                         company_id=temp_data.company_id,
                                                         branch_id=temp_data.branch_id,
                                                         small_wood=temp_data.small_wood,
                                                         medium_wood=temp_data.medium_wood,
                                                         large_wood=temp_data.large_wood,
                                                         total_wood=temp_data.total_wood,
                                                         discard_wood=temp_data.discard_wood,
                                                         original_pic=temp_data.original_pic,
                                                         detected_pic=temp_data.detected_pic,
                                                         dateupload=temp_data.dateupload,
                                                         small_volume=temp_data.small_volume,
                                                         medium_volume=temp_data.medium_volume,
                                                         large_volume=temp_data.large_volume,
                                                         total_volume=temp_data.total_volume,
                                                         onechat_id=temp_data.onechat_id,
                                                         volume=temp_data.volume,
                                                         comment=temp_data.comment,
                                                         small_wood_edit=temp_data.small_wood_edit,
                                                         medium_wood_edit=temp_data.medium_wood_edit,
                                                         large_wood_edit=temp_data.large_wood_edit,
                                                         total_wood_edit=temp_data.total_wood_edit,
                                                         small_volume_edit=temp_data.small_volume_edit,
                                                         medium_volume_edit=temp_data.medium_volume_edit,
                                                         large_volume_edit=temp_data.large_volume_edit,
                                                         total_volume_edit=temp_data.total_volume_edit,
                                                         lot_id=temp_data.lot_id,
                                                         license_plate=temp_data.license_plate,
                                                         backup_pic = temp_data.backup_pic)
                        sess.add(create_history)

                        sess.delete(temp_data)
                        sess.commit()
                        sent_text(user_id=user_id , bot_id=bot_id , messege="OK ฉันบันทึกผลการตรวจจับลงในระบบให้เรียบร้อยแล้ว")
                        quickreply_forend(user_id=user_id , bot_id=bot_id , one_id=one_id, lot_id=data['message']['data']['lot_id'])
                    elif 'notconfirm' in data['message']['data']:
                        print("case not confirm")
                        temp_data = table_temp_history.query.filter_by(id=data['message']['data']['notconfirm']).first()
                        sess.delete(temp_data)
                        sess.commit()
                        sent_text(user_id=user_id, bot_id=bot_id, messege="OK ฉันลบผลการตรวจจับออกจากระบบให้เรียบร้อยแล้ว")
                        quickreply_forend(user_id=user_id, bot_id=bot_id, one_id=one_id, lot_id=data['message']['data']['lot_id'])
                    elif 'success' in data['message']['data']:
                        history_data = table_history.query.filter_by(lot_id=data['message']['data']['success']).all()
                        total_small = 0
                        total_medium = 0
                        total_large = 0
                        total_total = 0
                        total_discard = 0
                        total_small_volume = 0
                        total_medium_volume = 0
                        total_large_volume = 0
                        total_total_volume = 0
                        for i in history_data:
                            small = None
                            medium = None
                            large = None
                            discard = None
                            small_volume = None
                            medium_volume = None
                            large_volume = None
                            total_volume = None

                            if i.small_wood_edit == None:
                                small = i.small_wood
                            else:
                                small = i.small_wood_edit

                            if i.medium_wood_edit == None:
                                medium = i.medium_wood
                            else:
                                medium = i.medium_wood_edit
                            if i.large_wood_edit == None:
                                large = i.large_wood
                            else:
                                large = i.large_wood_edit
                            if i.small_volume_edit == None:
                                small_volume = i.small_volume
                            else:
                                small_volume = i.small_volume_edit
                            if i.medium_volume_edit == None:
                                medium_volume = i.medium_volume
                            else:
                                medium_volume = i.medium_volume_edit
                            if i.large_volume_edit == None:
                                large_volume = i.large_volume
                            else:
                                large_volume = i.large_volume_edit

                            total_discard += int(i.discard_wood)
                            total_small += int(small)
                            total_medium += int(medium)
                            total_large += int(large)
                            total_total += int(small)+int(medium)+int(large)
                            total_small_volume += int(small_volume)
                            total_medium_volume += int(medium_volume)
                            total_large_volume += int(large_volume)
                            total_total_volume += int(small_volume) + int(medium_volume) +  int(large_volume)
                        table_lot.query.filter_by(id=data['message']['data']['success']).update({"small_wood":total_small ,
                                                                                                 "medium_wood":total_medium,
                                                                                                 "large_wood":total_large,
                                                                                                 "total_wood":total_total,
                                                                                                 "discard_wood":total_discard,
                                                                                                 "small_volume":total_small_volume,
                                                                                                 "medium_volume":total_medium_volume,
                                                                                                 "large_volume":total_large_volume,
                                                                                                 "total_volume":total_total_volume})
                        sess.commit()
                        sent_text(user_id=user_id, bot_id=bot_id,messege="เสร็จสิ้นกระบวนการตรวจจับแล้ว")
                else:
                    print("from one chat")
                    if data['message']['text'] == "ox":
                        print("if")
                    else:
                        print("else")
                        temp_data = table_temp_history.query.filter_by(onechat_id=user_id).all()
                        if temp_data == []:
                            user_data = table_users.query.filter_by(onechat_id=user_id).first()
                            company_data = table_company.query.filter_by(id=user_data.company_id).first()
                            # sand_template(user_id=user_id, bot_id=bot_id , one_id=one_id , lot_id=)
                            lot_id = datetime.datetime.now().strftime('%d%m%Y%H%M%S%f')[:-3]
                            quickreply_start(user_id=user_id, bot_id=bot_id, one_id=one_id ,lot_id=lot_id)
                        else:
                            for i in range(len(temp_data)):
                                # create_history = table_history(id=temp_data[i].id,
                                #                                users_id=temp_data[i].users_id,
                                #                                company_id=temp_data[i].company_id,
                                #                                branch_id=temp_data[i].branch_id,
                                #                                small_wood=temp_data[i].small_wood,
                                #                                medium_wood=temp_data[i].medium_wood,
                                #                                large_wood=temp_data[i].large_wood,
                                #                                total_wood=temp_data[i].total_wood,
                                #                                discard_wood=temp_data[i].discard_wood,
                                #                                original_pic=temp_data[i].original_pic,
                                #                                detected_pic=temp_data[i].detected_pic,
                                #                                dateupload=temp_data[i].dateupload,
                                #                                small_volume=temp_data[i].small_volume,
                                #                                medium_volume=temp_data[i].medium_volume,
                                #                                large_volume=temp_data[i].large_volume,
                                #                                total_volume=temp_data[i].total_volume,
                                #                                onechat_id=temp_data[i].onechat_id)
                                # sess.add(create_history)
                                lot = table_lot.query.filter_by(id=temp_data[i].lot_id).first()
                                if lot != None:
                                    sess.delete(lot)
                                    sess.commit()
                                sess.delete(temp_data[i])
                            sess.commit()
                            sent_text(user_id=user_id , bot_id=bot_id , messege="คุณไม่ได้ทำการยืนยันบางรายการให้ฉัน\nข้อมูลถูกลบออกจากระบบแล้ว")



            elif data['message']['type'] == 'image':
                sent_text(user_id=user_id, messege="กรุณาส่งรูปภาพผ่านทางแบบฟอร์มเท่านั้น !", bot_id=bot_id)
    sess.close()
    return json_response({"msg":"ok"})

