# -*- coding: utf-8 -*
from apps.webapp import controller
from ..helper.helper import *
print ('...start routing module api')
from flask import Blueprint

routes = Blueprint('/upload',__name__)

routes.add_url_rule(
    '',
    '',
    controller.aidetection,
    methods = ['POST']
)
routes.add_url_rule(
    'get',
    'gettemp',
    controller.gettemp,
    methods = ['GET']
)
routes.add_url_rule(
    'edit',
    'edittemp',
    controller.edittemp,
    methods = ['PUT']
)
routes.add_url_rule(
    'cancel',
    'cancel',
    controller.cancel_edit,
    methods = ['POST']
)


# quickreply_forend(user_id="U46caf077e7e05e9c902f15f7a7959a83",bot_id ="B41e192a6ba9a5eb3840d41839f20fe12",one_id="3148142722", lot_id="19032020102752406")
# print("password = " ,encryption_password("timber07"))
print ('...finish routing module api222')