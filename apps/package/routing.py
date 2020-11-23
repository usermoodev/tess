# -*- coding: utf-8 -*
from apps.package import controller

print ('...start routing package')
from flask import Blueprint

routes = Blueprint('/package',__name__)

routes.add_url_rule(
    '',
    'addpackage',
    controller.addpackage,
    methods = ['POST']
)
routes.add_url_rule(
    '',
    'getallpackage',
    controller.getallpackage,
    methods = ['GET']
)
routes.add_url_rule(
    '',
    'editpackage',
    controller.editpackage,
    methods = ['PUT']
)
routes.add_url_rule(
    '',
    'editpackage',
    controller.editpackage,
    methods = ['PUT']
)
routes.add_url_rule(
    '',
    'deletepackage',
    controller.deletepackage,
    methods = ['DELETE']
)











print ('...finish routing module package')