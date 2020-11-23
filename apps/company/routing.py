# -*- coding: utf-8 -*
from apps.company import controller

print ('...start routing module api')
from flask import Blueprint

routes = Blueprint('/company',__name__)

routes.add_url_rule(
    '',
    'addcompany',
    controller.addcompany,
    methods = ['POST']
)
routes.add_url_rule(
    '',
    'update_company',
    controller.update_company,
    methods = ['PUT']
)
routes.add_url_rule(
    'addadmin',
    'add_admin',
    controller.add_admin,
    methods = ['POST']
)
routes.add_url_rule(
    'deleteadmin',
    'delete_admin',
    controller.delete_admin,
    methods = ['DELETE']
)
routes.add_url_rule(
    'updateadmin',
    'update_admin',
    controller.update_admin,
    methods = ['PUT']
)
routes.add_url_rule(
    '',
    'getallcompany',
    controller.getallcompany,
    methods = ['GET']
)
routes.add_url_rule(
    '',
    '',
    controller.delete_company,
    methods = ['DELETE']
)



print ('...finish routing module api222')