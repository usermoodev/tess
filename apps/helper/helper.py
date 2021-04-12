import hashlib
from flask import Response , json
import urllib3
import urllib.request
import base64
import requests
import jwt
from ..app import *
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from requests_toolbelt.multipart.encoder import MultipartEncoder
key = "l;ylfu8iy["
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
ref_code = "Af3ZG6"
client_id = "181"
client_secret = "WpV9gm7QObhSJmYoaREC0DACUGxsN5pMpIZf7z2L"

DOMAIN_WEBVIEW = os.getenv('DOMAIN_WEBVIEW', default="http://localhost:8081")

def encryption_password(password):
    s = str(password)
    shaHash = hashlib.sha256(s.encode('utf-8'))
    encrypt_password = shaHash.hexdigest()
    return encrypt_password

def dowload_image(url , filepath , filename):
    fullpath = filepath+filename+'.jpg'
    urllib.request.urlretrieve(url,fullpath)

def createBase64(filepath , filename):
    fullpath = filepath+filename+'.jpg'
    with open("{}".format(fullpath), "rb") as img_file:
        base64encode = base64.b64encode(img_file.read())
        substrbase64 = str(base64encode).replace("b'", "")
        substrbase64_2 = substrbase64.replace("'", "")
    os.remove(fullpath)
    return substrbase64_2

def createBase64webveiw(filepath , filename):
    fullpath = filepath+filename
    with open("{}".format(fullpath), "rb") as img_file:
        base64encode = base64.b64encode(img_file.read())
        substrbase64 = str(base64encode).replace("b'", "")
        substrbase64_2 = substrbase64.replace("'", "")
    # os.remove(fullpath)
    return substrbase64_2

def createimages(data_base64,filename):
    fullpath = photopath + filename + ".jpg"
    with open(fullpath, "wb") as fh:
        fh.write(base64.b64decode(data_base64))
    # print ("fullpath in createimages >> ",fullpath)
    return fullpath

def createimageswebveiw(data_base64,filename , user_id):
    fullpath = photopath + str(user_id) + "/" + filename
    with open(fullpath, "wb") as fh:
        fh.write(base64.b64decode(data_base64))
    # print ("fullpath in createimages >> ",fullpath)
    return fullpath

def detecttimber(base64,small_case , medium_case , large_case,bot_id):
    # print (base64[:20])
    try:
        url = "http://quanta2.manageai.co.th:3333/api/v1/detection"
        payload = {"img":base64 ,
                   "small_case":float(small_case),
                   "medium_case":float(medium_case),
                   "large_case":float(large_case),
                   "user":"doublea"}
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        print("Wait.. AI")
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers ,verify=False)
        print("Respnone from AI")

        return response.json()

    # print (response.text)
    except:
        print("AI fail from script")
        sand_text_group(bot_id,"++ AI ตรวจจับท่อนไม้มีปัญหากรุณาตรวจสอบด่วน ++")

def detecttimberwebveiw(base64,small_case , medium_case , large_case,bot_id , length_wood):
    # print (base64[:20])
    try:
        url = "http://quanta2.manageai.co.th:3333/api/v1/detection"
        payload = {"img":base64 ,
                   "small_case":float(small_case),
                   "medium_case":float(medium_case),
                   "large_case":float(large_case),
                   "user":"doublea",
                   "length_wood":length_wood}
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        print("Wait.. AI")
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers ,verify=False)
        print("Respnone from AI")

        return response.json()

    # print (response.text)
    except:
        print("AI fail from script")
        sand_text_group(bot_id,"++ AI ตรวจจับท่อนไม้มีปัญหากรุณาตรวจสอบด่วน ++")

def sand_text_group(bot_id,message):

    url = "https://chat-public.one.th:8034/api/v1/push_message"
    payload = {
        "to":"G5e34fc671c150a00299a31b7b14dafba89d05ceca7d4e30a37a3944f",
        "bot_id": bot_id,
        "email_business":"jarindeveloper@one.th",
        "type": "text",
        "message": message
    }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def sent_text(user_id,messege , bot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_message"
    payload =  {"to" : user_id,
                "bot_id" : bot_id,
                "type" : "text",
                 "message" : messege
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers ,verify=False)

    # print("sent success ")

def quickreply_forend(user_id,bot_id  ,one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "ท่านมีรูปภาพอื่นให้ตรวจจับอีกหรือไม่ ?",
               "quick_reply" : [{"label": "ตรวจจับท่อนไม้(ต่อ)",
                                 "type": "webview",
                                 "url": DOMAIN_WEBVIEW + "/upload?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id,
                                 "size": "full"},
                                {"label": "เสร็จสิ้น",
                                 "type": "text",
                                 "message": "เสร็จสิ้นกระบวนการ",
                                 "payload": {"success": lot_id}
                                 }
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    print("for end >>>>> " + DOMAIN_WEBVIEW + "/upload?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def quickreply_edit(user_id,bot_id , temp_id , one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "ฉันแก้ไขข้อมูลให้แล้ว \nคุณต้องการทำอะไรต่อ ?",
               "quick_reply" : [{"label" : "ยืนยันผลการตรวจจับ",
                                 "type" : "text",
                                 "message" : "ฉันต้องการยืนยัน",
                                 "payload" : { "confirm": temp_id,
                                               "lot_id":lot_id}},
                                {"label": "แก้ไขผลการตรวจจับ(อีกครั้ง)",
                                 "type": "webview",
                                 "url":DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id,
                                 "size": "full"},
                                {"label": "ลบผลการตรวจจับ",
                                 "type": "text",
                                 "message": "ฉันต้องการลบ",
                                 "payload": {"notconfirm": temp_id,
                                             "lot_id":lot_id}}
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    print("cancel edit >>>>>>>>>>>>>>>>>>>>> ")
    print(DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def quickreply_canceledit(user_id,bot_id , temp_id , one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "ฉันแก้ไขข้อมูลให้แล้ว \nคุณต้องการทำอะไรต่อ ?",
               "quick_reply" : [{"label" : "ยืนยันผลการตรวจจับ",
                                 "type" : "text",
                                 "message" : "ฉันต้องการยืนยัน",
                                 "payload" : { "confirm": temp_id,
                                               "lot_id":lot_id}},
                                {"label": "แก้ไขผลการตรวจจับ(อีกครั้ง)",
                                 "type": "webview",
                                 "url": DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id,
                                 "size": "full"},
                                {"label": "ลบผลการตรวจจับ",
                                 "type": "text",
                                 "message": "ฉันต้องการลบ",
                                 "payload": {"notconfirm": temp_id,
                                             "lot_id":lot_id}}
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    print(DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def quickreply_inprocess(user_id,bot_id , temp_id , one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    print("quck reply inprocess")
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "ผลการตรวจจับของฉัน\nเป็นที่พอใจหรือไม่ ? " +
                            "\nช่วยยืนยันให้ฉันหน่อยสิ",
               "quick_reply" : [{"label" : "ยืนยันผลการตรวจจับ",
                                 "type" : "text",
                                 "message" : "ฉันต้องการยืนยัน",
                                 "payload" : { "confirm": temp_id ,
                                               "lot_id":lot_id}},
                                {"label": "แก้ไขผลการตรวจจับ",
                                 "type": "webview",
                                 "url": DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id,
                                 "size": "full"},
                                {"label": "ลบผลการตรวจจับ",
                                 "type": "text",
                                 "message": "ฉันต้องการลบ",
                                 "payload": {"notconfirm": temp_id,
                                             "lot_id":lot_id}}
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    print(DOMAIN_WEBVIEW + "/edit?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id + "&temp_id=" + temp_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)


def quickreply_start(user_id,bot_id , one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "ไม่พบคำสั่ง ท่านต้องการจะทำอะไร ?",
               "quick_reply" : [
                                {"label": "ตรวจจับท่อนไม้",
                                 "type": "webview",
                                 "url": DOMAIN_WEBVIEW + "/upload?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id,
                                 "size": "full"}
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    print(DOMAIN_WEBVIEW + "/upload?user_id=" + user_id + "&bot_id=" + bot_id +"&one_id=" + one_id  + "&lot_id=" + lot_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def quickreply_comfirm(user_id,bot_id , temp_id):
    url = "https://chat-public.one.th:8034/api/v1/push_quickreply"
    payload = {"to" : user_id,
               "bot_id" : bot_id,
               "message" : "กรุณายืนยันอีกครั้งเพื่อบันทึกลงระบบ",
               "quick_reply" : [{"label" : "ยืนยันผลการตรวจจับ",
                                 "type" : "text",
                                 "message" : "ฉันต้องการยืนยัน",
                                 "payload" : { "confirm": temp_id}},
                                {"label": "ลบผลการตรวจจับ",
                                 "type": "text",
                                 "message": "ฉันต้องการลบ",
                                 "payload": {"notconfirm": temp_id}}
                                ]
                 }
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    # print("http://203.150.199.82:8050/form-edit-timber/" + user_id + "/" + bot_id +"/" + temp_id  + "/" + one_id)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def sand_template(user_id,bot_id , one_id , lot_id):
    url = "https://chat-public.one.th:8034/api/v1/push_message"
    payload = {"to": user_id,
               "bot_id": bot_id,
               "type": "template",
               "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา",
               "elements": [{"image": "https://chat-manage.one.th:8997/getpictureprofile/pYUbE8t4tCB16d96005a2fe52a292f3bf98267e4415_2020-02-01_15:37:38:050592.jpg",
                             "title": "ตรวจจับท่อนไม้",
                             "detail": "ใส่รายละเอียดสำหรับตรวจจับท่อนไม้",
                             "choice": [{"label": "กรอกข้อมูล",
                                         "type": "webview",
                                         # "url": "http://www.google.com",
                                         # "url": "http://203.150.199.82:8040/form-select?user_id="+user_id+"&bot_id="+bot_id,
                                         "url": DOMAIN_WEBVIEW + "/form-select/" + user_id+"/"+bot_id + "/" +one_id + "/" + lot_id,
                                         "size": "full"}]
                             }]
               }
    # print(payload['elements'][0]['choice'][0]['url'])
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

def sent_image(user_id,bot_id,fullpath):
    print("send images to Onechat..")
    multipart_data = MultipartEncoder(
        fields={
            "to":user_id,
            "bot_id":bot_id,
            "type":"file",
            "file":("dataset.jpg",open(fullpath, 'rb'),"image/jpeg")
            })
    print("Wait Onechat..")
    response = requests.post(
    url = "https://chat-public.one.th:8034/api/v1/push_message",
    headers = {
                  "Content-Type": multipart_data.content_type,
                  "Authorization": "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a"
              },
    data = multipart_data,
    )
    print("Response from Onechat..")

def closewebview(user_id , bot_id):
    url = "https://chat-public.one.th:8034/api/v1/disable_webview"
    payload = {"user_id": user_id,
               "bot_id": bot_id,
               }
    # print(payload['elements'][0]['choice'][0]['url'])
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer Ab60ef48b8cd4545ba88046baa11a531aa32f8cf9bee548dcb63236e8d39728e33306f590c06b4e8991a9aa6511c8051a",
        'Host': "chat-public.one.th:8034"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
    # print(response)

def json_response(messages=None, status=None, headers=None):
    if headers == None:
        headers = dict()
    headers.update({"Content-Type": "application/json"})
    contents = json.dumps(messages).replace('\\\"', '')
    if(status == None):
        status = 200
    resp = Response(response=contents, headers=headers, status=int(status))
    return resp

def genToken(username):
    payload = {
        "username": username,
        "issue_date": datetime.datetime.now().isoformat(),
    }

    token = jwt.encode(
        payload,
        key,
        algorithm='HS256'
    )
    mytoken = token.decode("utf-8")
    return str(mytoken)

def registercitizen_api(data):
    url = "https://one.th/api/register_api"
    payload = {"account_title_th":data['account_title_th'],
               "first_name_th":data['first_name_th'],
               "last_name_th":data['last_name_th'],
               "username":data['username'],
               "password":data['password'],
               "mobile_no":data['mobile_no'],
               "ref_code":ref_code,
               "clientId":client_id,
               "secretKey":client_secret
               }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload),verify=False)
    return response.json()

def resetpassword_oneid(data):
    url = "https://one.th/api/send_otp_reset_password"
    payload = {"username":data['username'],
               "tel_no":data['phone'],
               "refcode":ref_code,
               "client_id":client_id,
               "secretkey":client_secret
               }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload),verify=False)
    return response.json()

def resetpassword_by_otp(data):
    url = "https://one.th/api/reset_password_by_otp"
    payload = {"otp":data['otp'],
               "new_password":data['new_password'],
               "confirm_new_password":data['confirm_new_password'],
               "refcode":ref_code,
               "client_id":client_id,
               "secretkey":client_secret
               }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload),verify=False)
    return response.json()

def logincitizen(username,password):
    url = "https://one.th/api/oauth/getpwd"
    # urldemo= ""
    payload = {"grant_type":"password",
               "client_id":client_id,
               "client_secret":client_secret,
               "username":username,
               "password":password}
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload) ,verify=False)
    # print(response.json())
    return response.json()




def sendMail(company_name ,username , password , emailto):
    fromaddr = "contact@manageai.co.th"
    toaddr = str(emailto)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "แจ้งการเปิดใช้งานระบบ ตรวจับท่อนไม้"
    html = """    
    <html>
        <head>
            <style>
                table,
                th,td {
                    border: 3px solid black;
                    border-collapse: collapse;
                }
                th,td {
                    padding: 5px;
                    text-align: ;
                }
            </style>
        </head>
        <body>
            เรียน บริษัท  """ +company_name+ """
            <table>

                <tr>
                    <td>ระบบได้สร้างรหัสเข้าใช้งานของบริษัทท่านแล้ว\n
                    โดยสามารถใช้ user/password ดังนี้เพื่อเข้าใช้งานระบบ</td>
                </tr>
                <tr>
                </tr>
                <tr>
                    <td> username : """ + username + """</td>
                </tr>
                <tr>
                    <td> password : """ + password + """</td>
                </tr>
                <tr>
                    <td> URL : http://timber.manageai.co.th/</td>
                </tr>
               
            </table>
            หากมีข้อสงสัยสามารถติดต่อมาได้ที่ contact@manageai.co.th
        </body>
    </html>
            """
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    server = smtplib.SMTP('mailtx.inet.co.th', 25)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    server.quit()

def sendMailForgetpassword(data,randompassword):
    urldemo = "https://cxr.demo.sdi.inet.co.th"
    urlprod = "https://cxrservice.sdi.inet.co.th"
    username = data['username']
    password = randompassword
    fromaddr = "contact@manageai.co.th"
    # toaddr = "nt.natthaphon@gamil.com"
    toaddr = data['email']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "แจ้งเปลี่ยน Password สำหรับเข้าระบบ ตรวจจับท่อนไม้"
    html = """    
    <html>
        <head>
            <style>
                table,
                th,td {
                    border: 3px solid black;
                    border-collapse: collapse;
                }
                th,td {
                    padding: 5px;
                    text-align: ;
                }
            </style>
        </head>
        <body>
            เรียน ผู้ใช้งาน<br>
            เราได้ทำการresetpasswordให้คุณแล้ว
            <table>
                <tr>
                    <td> Username :</td>
                    <td>""" + username + """</td>
                </tr>
                <tr>
                    <td>Password :</td>
                    <td>""" + password + """</td>
                </tr>
            </table>
            หากมีข้อสงสัยสามารถติดต่อมาได้ที่ contact@manageai.co.th
        </body>
    </html>
            """
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    # server = smtplib.SMTP('mailout.inet.co.th', 25)
    server = smtplib.SMTP('mailtx.inet.co.th', 25)
    # (fromaddr, "0922681286")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def sendMail_adduser(username, password, emailto):

    fromaddr = "contact@manageai.co.th"
    toaddr = str(emailto)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "แจ้งการเปิดใช้งานระบบ ตรวจับท่อนไม้"
    html = """    
    <html>
        <head>
            <style>
                table,
                th,td {
                    border: 3px solid black;
                    border-collapse: collapse;
                }
                th,td {
                    padding: 5px;
                    text-align: ;
                }
            </style>
        </head>
        <body>
            เรียน บริษัท  ผู้ใช้งาน
            <table>

                <tr>
                    <td>admin ได้สร้างรหัสเข้าใช้งานของท่านแล้ว\n
                    โดยสามารถใช้ user/password ดังนี้เพื่อเข้าใช้งานแอปพลิเคชั่น onechat</td>
                </tr>
                <tr>
                </tr>
                <tr>
                    <td> username : """ + username + """</td>
                </tr>
                <tr>
                    <td> password : """ + password + """</td>
                </tr>
                <tr>
                    <td> โดยท่าน สามารถ dowload แอปพลิเคชั่นได้จาก appstore / playstore \n
                    หลังจากนั้น login และแอด bot ที่ชื่อว่า timber เพื่อใช้งานได้เลยครับ</td>
                </tr>

            </table>
            หากมีข้อสงสัยสามารถติดต่อมาได้ที่ contact@manageai.co.th
        </body>
    </html>
            """
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    server = smtplib.SMTP('mailtx.inet.co.th', 25)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

    server.quit()