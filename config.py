import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'hard to guess string'
    # SECRET_KEY = 'hard to guess string'
    SECRET_KEY = os.urandom(24)
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    db_name = 'ticket'
    my_password = ''
    my_db_conn = 'mysql+pymysql://root:%s@localhost:3306/%s?charset=utf8' % (my_password, db_name)
    per_page = 2
    UPLOADED_STADIUMIMGS_DEST = os.getcwd() + '/app/static/stadiumImgs'
    UPLOADED_SHOWIMGS_DEST = os.getcwd() + '/app/static/showImgs'
    UPLOADED_SHOWDESCFILES_DEST = os.getcwd() + '/app/static/descFiles'
    UPLOADED_ARTISTIMGS_DEST = os.getcwd() + '/app/static/artistImgs'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'dev')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'test')



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

