from flask import Flask
# from flask import Session
from flask.ext.session import Session
from redis import Redis
from flask_session import RedisSessionInterface

app = Flask(__name__, template_folder='templates', static_folder='statics', static_url_path='/statics')
app.secret_key = 'mros'
app.debug = True

# conn = Redis(host='10.0.0.10',port='6379')
# app.session_interface = RedisSessionInterface(conn,key_prefix='__',use_signer=False)

# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = Redis(host='10.0.0.10', port='6379')
# Session(app)


from .views.login import account
from .views.index import index

app.register_blueprint(account)
app.register_blueprint(index)
