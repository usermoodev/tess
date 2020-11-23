# -*- coding: utf-8 -*
print ('start init routing')
from .app import app
from .users.routing import routes as users
from .webhook.routing import routes as webhook
from .authen.routing import routes as authen
from .company.routing import routes as  company
from .package.routing import routes as package
from .branch.routing import routes as branch
from  .webapp.routing import routes as webapp
from .history.routing import routes as history
def root_endpoint():
    return 'WOOD-DETECTION'

def init_routes():
    app.add_url_rule( '/',
                      'root_endpoint',
                      root_endpoint,
                      methods=['GET'],
                    )
    app.register_blueprint(users , url_prefix="/api/v1/users")
    app.register_blueprint(authen , url_prefix="/api/v1/authen")
    app.register_blueprint(company , url_prefix="/api/v1/company")
    app.register_blueprint(package , url_prefix="/api/v1/package")
    app.register_blueprint(branch , url_prefix="/api/v1/branch")
    app.register_blueprint(webapp , url_prefix="/api/v1/upload")
    app.register_blueprint(history , url_prefix="/api/v1/history")
    app.register_blueprint(webhook , url_prefix="/api/v1/webhook")
print ('finish init routing')