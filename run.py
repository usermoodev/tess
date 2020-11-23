from apps.routes import init_routes
from apps.database import *
from apps.app import app

api_run = '0.0.0.0'
from datetime import *




init_routes()
createdatabase()



app.run(host=api_run, debug=True ,port=4242 )
