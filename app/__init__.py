from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class, TEXT
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from config import Config

csrf = CSRFProtect()

app = Flask(__name__)
app.config.from_object(Config)
csrf.init_app(app)
bootstrap = Bootstrap(app)

stadiumImgs = UploadSet('STADIUMIMGS', IMAGES)
showImgs = UploadSet('SHOWIMGS',IMAGES)
artistImgs = UploadSet('ARTISTIMGS',IMAGES)
showDescFiles = UploadSet('SHOWDESCFILES',TEXT)
configure_uploads(app, stadiumImgs)
configure_uploads(app, showImgs)
configure_uploads(app, showDescFiles)
configure_uploads(app, artistImgs)
# set maximum file size, default is 16MB
patch_request_class(app, 8*1024*1024)


from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from app.home import home as home_blueprint
app.register_blueprint(home_blueprint, url_prefix='')







