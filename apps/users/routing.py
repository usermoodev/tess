# -*- coding: utf-8 -*
from apps.users import controller
from ..database import *
print ('...start routing module api')
from flask import Blueprint

routes = Blueprint('/users',__name__)
routes.add_url_rule(
    'admin',
    'admin',
    controller.register_admin,
    methods = ['POST']
)
routes.add_url_rule(
    'superadmin',
    'superadmin',
    controller.register_superadmin,
    methods = ['POST']
)
routes.add_url_rule(
    '',
    '',
    controller.getallmember,
    methods = ['GET']
)
routes.add_url_rule(
    'register',
    'register',
    controller.register_user,
    methods = ['POST']
)
routes.add_url_rule(
    '',
    'updateuser',
    controller.update_user,
    methods = ['PUT']
)
routes.add_url_rule(
    '',
    'deleteuser',
    controller.delete_user,
    methods = ['DELETE']
)
routes.add_url_rule(
    'resetpassword',
    'resetpassword_user',
    controller.resetpassword_user,
    methods = ['POST']
)
routes.add_url_rule(
    'otp',
    'resetpassword_user_otp',
    controller.resetpassword_user_otp,
    methods = ['POST']
)






print ('...finish routing module api222')