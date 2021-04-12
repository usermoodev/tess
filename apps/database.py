# -*- coding: utf-8 -*
from .app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import backref, relationship
import mysql.connector
import uuid
import json
import time
import sys
from sqlalchemy import and_
from pandas import DataFrame
import datetime
print("start init database..")
import os


mydb_name = 'wood_detection'

host = 'localhost'
user = 'root'
password = ''

argv = sys.argv
if len(argv) > 1:
    if argv[1] == '--prod':
        DB_HOST = os.getenv('DB_HOST', default="172.24.7.230")
        DB_PORT = os.getenv('DB_PORT', default="31444")
        DB_USER = os.getenv('DB_USER', default="admin")
        DB_PASSWORD = os.getenv('DB_PASSWORD', default="admin")
        DB_NAME = os.getenv('DB_NAME', default="wood_detection")


# mydb = mysql.connector.connect(host=host, user=user, password=password)
# cur = mydb.cursor()
# cur.execute("SHOW DATABASES")
# db_list = []
# for db_name in cur:
#     db_list.append(db_name[0])
# if mydb_name not in db_list:
#     cur.execute("CREATE DATABASE " + mydb_name + " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8'.format(user, password, host,mydb_name)
# db = SQLAlchemy(app)



# >>> postgres <<<
# 203.150.221.101
# port: 31444
# user: admin
# pass: admin
# db: pgchicken

# >>> Dashboard <<<
# 203.150.221.101
# server: pg-chicken
# port: 30123
# user: admin
# pass: admin
# db: pgchicken

DB_HOST = os.getenv('DB_HOST', default="203.151.56.230")
DB_PORT = os.getenv('DB_PORT', default="31444")
DB_USER = os.getenv('DB_USER', default="admin")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="admin")
DB_NAME = os.getenv('DB_NAME', default="wood_detection")


url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print("connect sucess {}".format(url))
app.config['SQLALCHEMY_DATABASE_URI']= url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = os.getenv('SQLALCHEMY_POOL_SIZE', default=100)
app.config['SQLALCHEMY_POOL_TIMEOUT'] = os.getenv('SQLALCHEMY_POOL_TIMEOUT', default=300)


db = SQLAlchemy(app)


def generate_uuid():
    uid = uuid.uuid4()
    return str(uid)[:8]


class table_admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.String(8), primary_key=True,default=generate_uuid)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    company_id = db.Column(db.String(8), db.ForeignKey("company.id", ondelete="cascade"))
    company_id_ref = db.relationship("table_company", lazy=True ,backref=backref('admin', cascade="all,delete"))

class table_branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    company_id = db.Column(db.String(8), db.ForeignKey("company.id", ondelete="cascade"))
    company_id_ref = db.relationship("table_company", backref=backref('branch', cascade="all,delete"), lazy=True)


class table_company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    name  = db.Column(db.String(255))
    address = db.Column(db.String(255))
    small_case = db.Column(db.String(255))
    medium_case =  db.Column(db.String(255))
    large_case =  db.Column(db.String(255))



class table_history(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    company_id  = db.Column(db.String(8) , db.ForeignKey("company.id" , ondelete="cascade"))
    company_id_ref = db.relationship("table_company", backref=backref('history', cascade="all,delete") , lazy=True)
    branch_id  = db.Column(db.String(8), db.ForeignKey("branch.id" , ondelete="cascade"))
    branch_id_ref = db.relationship("table_branch", backref=backref('history', cascade="all,delete"), lazy=True)
    users_id = db.Column(db.String(8), db.ForeignKey("users.id" , ondelete="cascade"))
    user_id_ref = db.relationship("table_users", backref=backref('history', cascade="all,delete"), lazy=True)
    small_wood = db.Column(db.Integer)
    medium_wood = db.Column(db.Integer)
    large_wood = db.Column(db.Integer)
    total_wood = db.Column(db.Integer)
    large_wood = db.Column(db.Integer)
    discard_wood = db.Column(db.Integer)
    original_pic = db.Column(db.String(255))
    detected_pic = db.Column(db.String(255))
    dateupload = db.Column(db.DateTime(255))
    small_volume = db.Column(db.String(10))
    medium_volume = db.Column(db.String(10))
    large_volume = db.Column(db.String(10))
    total_volume = db.Column(db.String(10))
    onechat_id = db.Column(db.String(255))
    volume = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    small_wood_edit = db.Column(db.Integer)
    medium_wood_edit = db.Column(db.Integer)
    large_wood_edit = db.Column(db.Integer)
    total_wood_edit = db.Column(db.Integer)
    small_volume_edit = db.Column(db.Integer)
    medium_volume_edit = db.Column(db.Integer)
    large_volume_edit = db.Column(db.Integer)
    total_volume_edit = db.Column(db.Integer)
    lot_id = db.Column(db.String(8), db.ForeignKey("lot.id", ondelete="cascade"))
    lot_id_ref = db.relationship("table_lot", backref=backref('history', cascade="all,delete"), lazy=True)
    license_plate = db.Column(db.String(255))
    length_wood = db.Column(db.Float)
    backup_pic = db.Column(db.String(255))

class table_temp_history(db.Model):
    __tablename__ = 'temp_history'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    company_id  = db.Column(db.String(8))
    branch_id  = db.Column(db.String(8))
    users_id = db.Column(db.String(8))
    small_wood = db.Column(db.Integer)
    medium_wood = db.Column(db.Integer)
    large_wood = db.Column(db.Integer)
    total_wood = db.Column(db.Integer)
    large_wood = db.Column(db.Integer)
    discard_wood = db.Column(db.Integer)
    original_pic = db.Column(db.String(255))
    detected_pic = db.Column(db.String(255))
    dateupload = db.Column(db.DateTime(255))
    small_volume = db.Column(db.String(10))
    medium_volume = db.Column(db.String(10))
    large_volume = db.Column(db.String(10))
    total_volume = db.Column(db.String(10))
    onechat_id = db.Column(db.String(255))
    volume = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    small_wood_edit = db.Column(db.Integer)
    medium_wood_edit = db.Column(db.Integer)
    large_wood_edit = db.Column(db.Integer)
    total_wood_edit = db.Column(db.Integer)
    small_volume_edit = db.Column(db.Integer)
    medium_volume_edit = db.Column(db.Integer)
    large_volume_edit = db.Column(db.Integer)
    total_volume_edit = db.Column(db.Integer)
    lot_id = db.Column(db.String(8), db.ForeignKey("lot.id", ondelete="cascade"))
    lot_id_ref = db.relationship("table_lot", backref=backref('temp_history', cascade="all,delete"), lazy=True)
    license_plate = db.Column(db.String(255))
    length_wood = db.Column(db.Float)
    backup_pic = db.Column(db.String(255))

class table_package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    name  = db.Column(db.String(255))
    price  = db.Column(db.Integer)
    counting = db.Column(db.String(255))

class table_users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    username  = db.Column(db.String(255))
    password  = db.Column(db.String(255))
    account_title_th =  db.Column(db.String(255))
    first_name_th = db.Column(db.String(255))
    last_name_th = db.Column(db.String(255))
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    company_id = db.Column(db.String(8), db.ForeignKey("company.id" , ondelete="cascade"))
    company_id_ref = db.relationship("table_company",  backref=backref('users', cascade="all,delete"), lazy=True)
    branch_id = db.Column(db.String(8), db.ForeignKey("branch.id" , ondelete="cascade"))
    branch_id_ref = db.relationship("table_branch", backref=backref('users', cascade="all,delete"), lazy=True)
    one_id = db.Column(db.String(255))
    onechat_id = db.Column(db.String(255))

class table_company_package(db.Model):
    __tablename__ = 'company_package'
    id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
    start_date  = db.Column(db.String(255))
    end_date  = db.Column(db.String(255))

    package_id = db.Column(db.String(8) , db.ForeignKey("package.id" , ondelete="cascade"))
    pack_id_ref = db.relationship("table_package" ,  backref=backref('company_package', cascade="all,delete"), lazy=True)

    company_id = db.Column(db.String(8), db.ForeignKey("company.id", ondelete='cascade'))
    company_pack = db.relationship("table_company", backref=backref('company_package', cascade="all,delete"), lazy=True)

class table_lot(db.Model):
    __tablename__ = 'lot'
    id = db.Column(db.String(17), primary_key=True)
    company_id = db.Column(db.String(8), db.ForeignKey("company.id", ondelete='cascade'))
    company_pack = db.relationship("table_company", backref=backref('lot', cascade="all,delete"), lazy=True)
    branch_id = db.Column(db.String(8), db.ForeignKey("branch.id", ondelete="cascade"))
    branch_id_ref = db.relationship("table_branch", backref=backref('lot', cascade="all,delete"), lazy=True)
    users_id = db.Column(db.String(8), db.ForeignKey("users.id", ondelete="cascade"))
    user_id_ref = db.relationship("table_users", backref=backref('lot', cascade="all,delete"), lazy=True)
    small_wood = db.Column(db.Integer)
    medium_wood = db.Column(db.Integer)
    large_wood = db.Column(db.Integer)
    total_wood = db.Column(db.Integer)
    discard_wood = db.Column(db.Integer)
    dateupload  = db.Column(db.DateTime(255))
    small_volume = db.Column(db.Integer)
    medium_volume = db.Column(db.Integer)
    large_volume = db.Column(db.Integer)
    total_volume = db.Column(db.Integer)
    license_plate = db.Column(db.String(255))


def createdatabase():
    db.create_all()
    # db.drop_all()




# class table_admin(db.Model):
#     __tablename__ = 'admin'
#     id = db.Column(db.String(8), primary_key=True,default=generate_uuid)
#     username = db.Column(db.String)
#     password = db.Column(db.String)
#     phone = db.Column(db.String)
#     email = db.Column(db.String)
#     role = db.Column(db.String)
#     access_token = db.Column(db.String)
#     company_id = db.Column(db.String)
#
# class table_branch(db.Model):
#     __tablename__ = 'branch'
#     id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
#     name = db.Column(db.String)
#     address = db.Column(db.String)
#     phone = db.Column(db.String)
#     company_id = db.Column(db.String(8))
#
#
# class table_company(db.Model):
#     __tablename__ = 'company'
#     id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
#     name  = db.Column(db.String)
#     address = db.Column(db.String)
#     small_case = db.Column(db.Integer)
#     medium_case =  db.Column(db.Integer)
#     large_case =  db.Column(db.Integer)
#
#
#
# class table_history(db.Model):
#     __tablename__ = 'history'
#     id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
#     company_id  = db.Column(db.String(8))
#     branch_id  = db.Column(db.String(8))
#     users_id = db.Column(db.String(33))
#     small_wood = db.Column(db.Integer)
#     medium_wood = db.Column(db.Integer)
#     large_wood = db.Column(db.Integer)
#     total_wood = db.Column(db.Integer)
#     large_wood = db.Column(db.Integer)
#     discard_wood = db.Column(db.Integer)
#     original_pic = db.Column(db.String)
#     detected_pic = db.Column(db.String)
#     date = db.Column(db.DateTime , default=datetime.datetime.now() + datetime.timedelta(minutes=7 * 60) )
#
#
# class table_package(db.Model):
#     __tablename__ = 'package'
#     id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
#     name  = db.Column(db.String)
#     price  = db.Column(db.Integer)
#     counting = db.Column(db.String)
#
# class table_users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.String(33), primary_key=True, default=generate_uuid)
#     username  = db.Column(db.String)
#     password  = db.Column(db.String)
#     account_title_th =  db.Column(db.String)
#     first_name_th = db.Column(db.String)
#     last_name_th = db.Column(db.String)
#     name = db.Column(db.String)
#     phone = db.Column(db.String)
#     email = db.Column(db.String)
#     company_id = db.Column(db.String(8))
#     branch_id = db.Column(db.String(8))
#     one_id = db.Column(db.String)
#     onechat_id = db.Column(db.String)
#
# class table_company_package(db.Model):
#     __tablename__ = 'company_package'
#     id = db.Column(db.String(8), primary_key=True, default=generate_uuid)
#     start_date  = db.Column(db.String)
#     end_date  = db.Column(db.String)
#     package_id = db.Column(db.String(8))
#     company_id = db.Column(db.String(8), db.ForeignKey("company.id", ondelete='cascade'))
#     company_pack = db.relationship("table_company", cascade="all,delete", backref="company_package", lazy=True)
