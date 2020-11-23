# -*- coding: utf-8 -*
from apps.webhook import controller

print ('...start routing module api')
from flask import Blueprint

routes = Blueprint('/webhook',__name__)
routes.add_url_rule(
    '',
    '',
    controller.webhook,
    methods = ['POST']
)



print ('...finish routing module api222')