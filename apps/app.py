# -*- coding: utf-8 -*
print ("..init apps")
from flask import Flask, render_template ,request
import os
import  sys

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
client_id = "154"
client_secret = "Z6R13WBGPUenh3dslfEjNdbaFkjp3My23A6VHy6W"
ref_code = "o7ZcR6"


photopath = "D:/INET/timber/image/"
export_path = "D:/INET/csv/"

argv = sys.argv
if len(argv) > 1:
    if argv[1] == '--prod':
        photopath = '/data/timber/image/'
        export_path = "/data/timber/csv/"
app = Flask(__name__)

# @app.after_request
# def after_request(response):
#     allow_origin_list = ['http://localhost:4200' , 'https://timber-webview-v2.manageai.co.th',"http://localhost:8080" ,'http://203.150.199.82:8040' ,'http://timber.manageai.co.th' , '203.154.135.179:8000' ,'http://203.150.199.82:8050','http://203.151.56.230:9010' , 'http://timber-v2.manageai.co.th','https://timber-v2.manageai.co.th','http://203.151.56.230:80' ,'http://203.151.56.230']
#
#     if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN']  in allow_origin_list:
#         response.headers.add('Access-Control-Allow-Origin', request.environ['HTTP_ORIGIN'] )
#         response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,Content-type,withCredentials,authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE')
#     return response
#

# app = Flask(__name__)
# @app.after_request
# def after_request(response):
#     allow_origin_list = ['http://localhost:4200' ,'http://timber-v2.manageai.co.th','http://203.151.56.230:80' ,'http://203.151.56.230']
#
#     if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN']  in allow_origin_list:
#         response.headers.add('Access-Control-Allow-Origin', request.environ['HTTP_ORIGIN'] )
#         response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With,Content-type,withCredentials,authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE')
#     return response
#

@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Origin',
        '*'
        # 'http://localhost:4200',
        # 'http://localhost:4100'

    )
    response.headers.add(
        'Access-Control-Allow-Credentials',
        'true'
    )
    response.headers.add(
        'Access-Control-Allow-Headers',
        'X-Requested-With,Content-type,withCredentials,authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE,OPTIONS'
    )

    return response




print ('..finish init apps')
