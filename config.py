from decouple import config


class Config:
    pass


class ProductionConfig(Config):
    DEBUG = False
    STATIC_FOLDER = "/static"
    TEMPLATE_FOLDER = "/templates"
    SECRET_KEY = config('SECRET_KEY', default='localhost')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL_USERNAME', default='localhost')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='localhost')
    DB_USER = config('DB_USER', default='localhost')
    DB_PASSWORD = config('DB_PASSWORD', default='localhost')
    DB_HOST = config('DB_HOST', default='localhost')
    DB_NAME = config('DB_NAME', default='localhost')
    DB_RIGHTS_WRITE = config('DB_RIGHTS_WRITE', default='localhost')
    DB_RIGHTS_MAJORITY = config('DB_RIGHTS_MAJORITY', default='localhost')
    DB_RIGHTS_SSL = config('DB_RIGHTS_SSL', default='localhost')
    DB_RIGHTS_SSL_CERT = config('DB_RIGHTS_SSL_CERT', default='localhost')
    F_KEY = config('F_KEY', default='localhost')

class DevelopmentConfig(Config):
    DEBUG = True
    STATIC_FOLDER = "/P2_VUE_WEBPACK/frontend/dist/static"
    TEMPLATE_FOLDER = "/P2_VUE_WEBPACK/frontend/dist"
    SECRET_KEY = "kdsfklsmfakfmafmadslvsdfasdf"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "webhook1example@gmail.com"
    MAIL_PASSWORD = "webhook123"
    DB_USER = "admin"
    DB_PASSWORD = "admin"
    DB_HOST = "cluster1.yj0k8.mongodb.net"
    DB_NAME = "mongo_db"
    DB_RIGHTS_WRITE = "retryWrites=true"
    DB_RIGHTS_MAJORITY = "w=majority"
    DB_RIGHTS_SSL = "ssl=true"
    DB_RIGHTS_SSL_CERT = "ssl_cert_reqs=CERT_NONE"
    F_KEY = "MLnwhktUDP-jhvcNHjO-uBPrDF7k1tqNbtA6Gk83dCg="


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
