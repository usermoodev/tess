# -*- coding: utf-8 -*
from apps.history import controller
from ..helper.helper import *
print ('...start routing module api')
from flask import Blueprint

routes = Blueprint('/history',__name__)

routes.add_url_rule(
    'lot',
    'getlot',
    controller.getlot,
    methods = ['GET']
)
routes.add_url_rule(
    'getdetail',
    'getdetail',
    controller.getdetailhistory,
    methods = ['GET']
)
routes.add_url_rule(
    'detaillot',
    'detaillot',
    controller.detaillot,
    methods = ['GET']
)
routes.add_url_rule(
    'superadmin',
    'gethistorysuperadmin',
    controller.gethistorysuperadmin,
    methods = ['GET']
)
routes.add_url_rule(
    'export',
    'exportcsv',
    controller.exportcsv,
    methods = ['POST']
)
routes.add_url_rule(
    'getuser',
    'getuser',
    controller.getuser,
    methods = ['POST']
)






# print("password = " ,encryption_password("timber07"))
print ('...finish routing module api222')