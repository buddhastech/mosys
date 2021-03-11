
class configDatabase(object):

    def __init__(self, app):
        __database_string = 'mysql+pymysql://diego:diegoduarteslipknot83@localhost/MOCIS'
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = __database_string
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
