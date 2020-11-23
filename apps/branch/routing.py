# -*- coding: utf-8 -*
from apps.branch import controller

print ('...start routing package')
from flask import Blueprint

routes = Blueprint('/branch',__name__)

routes.add_url_rule(
    '',
    'addpackage',
    controller.addbranch,
    methods = ['POST']
)
routes.add_url_rule(
    '',
    'getallbranch',
    controller.getallbranch,
    methods = ['GET']
)
routes.add_url_rule(
    '',
    'editbranch',
    controller.editbranch,
    methods = ['PUT']
)
routes.add_url_rule(
    '',
    'deletebranch',
    controller.deletebranch,
    methods = ['DELETE']
)










print ('...finish routing module package')